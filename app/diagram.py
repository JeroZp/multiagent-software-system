import subprocess


def generate_svg(input_path: str, output_path: str):

    try:

        cmd = f'mmdc -i "{input_path}" -o "{output_path}"'

        subprocess.run(
            cmd,
            shell=True,
            check=True,
            timeout=30
        )

        print("SVG generated:", output_path)

    except Exception as e:
        print("SVG generation failed:", e)
