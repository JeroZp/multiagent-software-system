# 🤖 Multi-Agent Software Engineering System

Sistema multi-agente para la generación automatizada de artefactos de ingeniería de software a partir de un brief de negocio, con soporte de **Human-in-the-Loop (HITL)**, control de estados y generación automática de diagramas.

Este proyecto fue desarrollado como parte de un reto académico de ingeniería de software basada en agentes inteligentes.

---

# 🚀 Características principales

* Pipeline multi-agente con etapas:

  * Requirements
  * Inception
  * User Stories
  * QA
  * Design
  * Done
* Control de estados persistente (RUNNING, WAITING_APPROVAL, COMPLETED, ERROR)
* Human-in-the-Loop (Approve / Reject / Feedback)
* Registro estructurado de decisiones (logs)
* Generación automática de artefactos JSON
* Generación automática de diagramas Mermaid y SVG
* Interfaz web para control del pipeline
* Persistencia de runs en base de datos SQLite
* Arquitectura extensible basada en agentes

---

# 🧠 Arquitectura del sistema

```
Frontend (HTML/JS)
        ↓
FastAPI Backend
        ↓
Multi-Agent Pipeline
        ↓
Artifacts + Logs + Database
```

Cada agente transforma el resultado del agente anterior:

```
Brief → Requirements → Inception → Stories → QA → Design
```

El sistema permite intervención humana en cualquier etapa.

---

# 🏗️ Tecnologías utilizadas

## Backend

* Python 3.10+
* FastAPI
* SQLAlchemy
* LangChain
* OpenAI API
* SQLite

## Frontend

* HTML
* CSS
* JavaScript (Vanilla)

## Diagramas

* Mermaid CLI
* Node.js

---

# 📂 Estructura del proyecto

```
project/
│
├── app/
│   ├── agents/
│   │   ├── requirements.py
│   │   ├── inception.py
│   │   ├── stories.py
│   │   ├── qa.py
│   │   └── design.py
│   │
│   ├── database.py
│   ├── models.py
│   ├── storage.py
│   ├── logger.py
│   ├── diagram.py
│   └── main.py
│
├── frontend/
│   └── index.html
│
├── runs/
│   └── (generated artifacts)
│
├── .env
├── requirements.txt
└── README.md
```

---

# ⚙️ Instalación

## 1️⃣ Clonar repositorio

```bash
git clone <repo-url>
cd project
```

---

## 2️⃣ Crear entorno virtual

```bash
python -m venv venv
```

Activar:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

---

## 3️⃣ Instalar dependencias Python

```bash
pip install -r requirements.txt
```

Si no existe requirements.txt:

```bash
pip install fastapi uvicorn sqlalchemy python-dotenv langchain langchain-openai
```

---

## 4️⃣ Configurar API Key de OpenAI

Crear archivo `.env`:

```
OPENAI_API_KEY=tu_api_key_aqui
```

---

# 🎨 Instalación de Mermaid (para SVG)

Instalar Node.js:

https://nodejs.org

Luego:

```bash
npm install -g @mermaid-js/mermaid-cli
```

Verificar:

```bash
mmdc -h
```

---

# ▶️ Ejecutar el sistema

## Backend

```bash
uvicorn app.main:app --reload
```

Servidor:

```
http://127.0.0.1:8000
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

## Frontend

Abrir:

```
frontend/index.html
```

en el navegador.

---

# 🔄 Flujo de uso

1. Ingresar brief en la interfaz
2. Start Run
3. Aprobar etapas progresivamente
4. Opcional: enviar feedback y regenerar
5. Pipeline llega a DONE

Artefactos generados en:

```
runs/{run_id}/
```

---

# 🧩 Ejemplo de Human-in-the-Loop

Feedback:

```
cambia REQ-002 a prioridad baja
```

Flujo:

```
Reject → Approve → Requirements regenerados
```

El sistema incorpora el feedback en la siguiente ejecución del agente.

---

# 📊 Artefactos generados

* brief.txt
* requirements.json
* inception.json
* stories.json
* testcases.json
* er.mmd
* sequence.mmd
* er.svg
* sequence.svg
* log.json

---

# 🧾 Logs de decisiones

Cada run contiene:

```
log.json
```

Incluye:

* timestamp
* agente
* etapa
* mensaje
* acciones humanas

Esto permite trazabilidad completa.

---

# 🧠 Estados del pipeline

```
CREATED
RUNNING
WAITING_APPROVAL
COMPLETED
ERROR
```

---

# 🧪 Endpoints principales

### Start run

```
POST /runs/start
```

### Approve stage

```
POST /runs/{id}/approve
```

### Reject stage

```
POST /runs/{id}/reject
```

### Status

```
GET /runs/{id}/status
```

### Artifacts

```
GET /runs/{id}/artifacts
```

### Logs

```
GET /runs/{id}/logs
```

---

# ⚠️ Troubleshooting

## Error: QueuePool limit reached

Solución: reiniciar servidor. Las sesiones DB se cierran automáticamente.

---

## Error: mmdc not found

Instalar:

```bash
npm install -g @mermaid-js/mermaid-cli
```

---

## SVG no se genera

Probar manual:

```bash
mmdc -i runs/test.mmd -o runs/test.svg
```

---

# 🔮 Posibles mejoras futuras

* Autenticación de usuarios
* Versionado de artefactos
* Exportación PDF
* Frontend React
* Orquestación con LangGraph
* Agentes adicionales (Architecture, DevOps)

---

# 👨‍💻 Autor

Proyecto académico — Sistema Multi-Agente de Ingeniería de Software.

---

# 📜 Licencia

Uso académico.
