from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from typing import Dict, Any

TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates"

env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=False)

def render_latex(data: Dict[str, Any]) -> str:
  tpl = env.get_template("resume.tex.j2")
  return tpl.render(**data)
