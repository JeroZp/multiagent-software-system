from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
import os
import json

from .database import Base, engine, SessionLocal
from .models import Run, StartRunRequest
from .storage import create_run_folder, save_text, save_json
from .logger import log_event

from .agents.requirements import requirements_agent
from .agents.inception import inception_agent
from .agents.design import design_agent
from .agents.qa import qa_agent
from .agents.stories import stories_agent

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================= ROOT =================

@app.get("/")
def root():
    return {"message": "Multi-Agent System Running"}


# ================= START RUN =================

@app.post("/runs/start")
def start_run(request: StartRunRequest):

    db = SessionLocal()

    try:

        brief = request.brief
        run_id = str(uuid4())

        run = Run(
            id=run_id,
            status="RUNNING",
            current_stage="requirements"
        )

        db.add(run)
        db.commit()

        create_run_folder(run_id)
        save_text(run_id, "brief.txt", brief)

        requirements = requirements_agent(brief)
        save_json(run_id, "requirements.json", requirements)

        log_event(run_id, "RequirementsAgent", "requirements",
                  "Requirements generated successfully")

        run.status = "WAITING_APPROVAL"
        db.commit()

        return {
            "run_id": run_id,
            "status": run.status,
            "stage": run.current_stage
        }

    except Exception as e:
        db.rollback()
        return {"error": str(e)}

    finally:
        db.close()


# ================= STATUS =================

@app.get("/runs/{run_id}/status")
def get_status(run_id: str):

    db = SessionLocal()

    try:
        run = db.query(Run).filter(Run.id == run_id).first()

        if not run:
            return {"error": "Run not found"}

        return {
            "run_id": run.id,
            "status": run.status,
            "stage": run.current_stage
        }

    finally:
        db.close()


# ================= ARTIFACTS =================

@app.get("/runs/{run_id}/artifacts")
def get_artifacts(run_id: str):

    path = f"runs/{run_id}"

    if not os.path.exists(path):
        return {"error": "Run not found"}

    return {
        "run_id": run_id,
        "files": os.listdir(path)
    }


# ================= APPROVE =================

@app.post("/runs/{run_id}/approve")
def approve_stage(run_id: str):

    db = SessionLocal()

    try:

        run = db.query(Run).filter(Run.id == run_id).first()

        if not run:
            return {"error": "Run not found"}

        if run.status != "WAITING_APPROVAL":
            return {"error": "Run not waiting approval"}

        run.status = "RUNNING"
        db.commit()

        # ===== REQUIREMENTS → INCEPTION =====
        if run.current_stage == "requirements":

            with open(f"runs/{run_id}/brief.txt", encoding="utf-8") as f:
                brief = f.read()

            feedback_path = f"runs/{run_id}/feedback.txt"

            feedback = None
            if os.path.exists(feedback_path):
                with open(feedback_path, encoding="utf-8") as f:
                    feedback = f.read()

            requirements = requirements_agent(brief, feedback)
            save_json(run_id, "requirements.json", requirements)

            log_event(run_id, "RequirementsAgent", "requirements",
                    "Requirements regenerated with feedback" if feedback else "Requirements generated")

            run.current_stage = "requirements"
            run.status = "WAITING_APPROVAL"

            with open(f"runs/{run_id}/requirements.json", encoding="utf-8") as f:
                requirements = json.load(f)

            inception = inception_agent(requirements)
            save_json(run_id, "inception.json", inception)

            log_event(run_id, "InceptionAgent", "inception",
                      "Inception document generated")

            run.current_stage = "inception"
            run.status = "WAITING_APPROVAL"

        # ===== INCEPTION → STORIES =====
        elif run.current_stage == "inception":

            with open(f"runs/{run_id}/requirements.json", encoding="utf-8") as f:
                requirements = json.load(f)

            with open(f"runs/{run_id}/inception.json", encoding="utf-8") as f:
                inception = json.load(f)

            stories = stories_agent(requirements, inception)
            save_json(run_id, "stories.json", stories)

            log_event(run_id, "StoriesAgent", "stories",
                      "User stories generated")

            run.current_stage = "stories"
            run.status = "WAITING_APPROVAL"

        # ===== STORIES → QA =====
        elif run.current_stage == "stories":

            with open(f"runs/{run_id}/stories.json", encoding="utf-8") as f:
                stories = json.load(f)

            testcases = qa_agent(stories)
            save_json(run_id, "testcases.json", testcases)

            log_event(run_id, "QAAgent", "qa",
                      "Test cases generated")

            run.current_stage = "qa"
            run.status = "WAITING_APPROVAL"

        # ===== QA → DESIGN =====
        elif run.current_stage == "qa":

            from .diagram import generate_svg

            with open(f"runs/{run_id}/requirements.json", encoding="utf-8") as f:
                requirements = json.load(f)

            with open(f"runs/{run_id}/stories.json", encoding="utf-8") as f:
                stories = json.load(f)

            with open(f"runs/{run_id}/testcases.json", encoding="utf-8") as f:
                testcases = json.load(f)

            diagrams = design_agent(requirements, stories, testcases)

            er_mmd = f"runs/{run_id}/er.mmd"
            seq_mmd = f"runs/{run_id}/sequence.mmd"

            er_svg = f"runs/{run_id}/er.svg"
            seq_svg = f"runs/{run_id}/sequence.svg"

            save_text(run_id, "er.mmd", diagrams["er"])
            save_text(run_id, "sequence.mmd", diagrams["sequence"])

            print("Generating SVG...")

            try:
                generate_svg(er_mmd, er_svg)
                generate_svg(seq_mmd, seq_svg)
            except Exception as e:
                print("SVG error:", e)

            print("SVG finished")

            log_event(run_id, "DesignAgent", "design",
                    "Dynamic diagrams generated")

            run.current_stage = "design"
            run.status = "WAITING_APPROVAL"

        # ===== DESIGN → DONE =====
        elif run.current_stage == "design":

            log_event(run_id, "System", "done",
                      "Pipeline completed successfully")

            run.current_stage = "done"
            run.status = "COMPLETED"

        db.commit()

        return {
            "run_id": run.id,
            "status": run.status,
            "stage": run.current_stage
        }

    except Exception as e:
        db.rollback()

        log_event(run_id, "System", run.current_stage,
          f"Error: {str(e)}")

        run.status = "ERROR"
        db.commit()

        print("Error during approval:", e)

        return {"error": str(e)}

    finally:
        db.close()


# ================= REJECT / FEEDBACK =================

@app.post("/runs/{run_id}/reject")
def reject_stage(run_id: str, feedback: str = "Rejected by user"):

    db = SessionLocal()

    try:

        run = db.query(Run).filter(Run.id == run_id).first()

        if not run:
            return {"error": "Run not found"}

        if run.status != "WAITING_APPROVAL":
            return {"error": "Run not waiting approval"}

        # 🔥 guardar feedback
        save_text(run_id, "feedback.txt", feedback)

        log_event(run_id, "Human", run.current_stage,
                  f"Stage rejected: {feedback}")

        run.status = "WAITING_APPROVAL"
        db.commit()

        return {
            "run_id": run.id,
            "status": "REJECTED",
            "stage": run.current_stage,
            "message": "Feedback saved. Approve again to regenerate."
        }

    finally:
        db.close()

# ================= LOGS =================

@app.get("/runs/{run_id}/logs")
def get_logs(run_id: str):

    path = f"runs/{run_id}/log.json"

    if not os.path.exists(path):
        return {"logs": []}

    with open(path) as f:
        data = json.load(f)

    return {
        "run_id": run_id,
        "logs": data
    }