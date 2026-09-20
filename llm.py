import subprocess


def generate_answer(prompt):
    result = subprocess.run(
        ["ollama", "run", "deepseek-r1:7b", "--hidethinking", prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )

    return result.stdout.strip()
