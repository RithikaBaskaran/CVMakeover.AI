from typing import Dict, Any, List
from .extract import extract_keywords

def score_bullet(bullet: str, keywords: List[str]) -> int:
  b = bullet.lower()
  return sum(1 for k in keywords if k in b)

def pick_top_bullets(items: List[Dict[str, Any]], keywords: List[str], max_total: int = 8):
  """
  Given projects/experience list with bullets, pick the most JD-relevant bullets overall.
  """
  scored = []
  for section_item in items:
    for bullet in section_item.get("bullets", []):
      scored.append((score_bullet(bullet, keywords), section_item, bullet))
  scored.sort(key=lambda x: x[0], reverse=True)

  chosen = []
  seen = set()
  for s, item, bullet in scored:
    key = (item.get("name") or item.get("org") or "", bullet)
    if key in seen:
      continue
    seen.add(key)
    if len(chosen) >= max_total:
      break
    chosen.append((item, bullet))
  return chosen

def tailor_profile(profile: Dict[str, Any], job_description: str) -> Dict[str, Any]:
  keywords = extract_keywords(job_description)

  # Copy profile shallowly
  out = dict(profile)
  out["jd_keywords"] = keywords

  # Re-rank skills: prioritize skills that appear in JD
  skills = profile.get("skills", [])
  skills_sorted = sorted(skills, key=lambda s: (s.lower() in " ".join(keywords)), reverse=True)
  out["skills"] = skills_sorted

  # Keep top bullets across experience + projects
  experience = profile.get("experience", [])
  projects = profile.get("projects", [])

  exp_top = pick_top_bullets(experience, keywords, max_total=6)
  proj_top = pick_top_bullets(projects, keywords, max_total=6)

  # Put selected bullets back grouped by item
  def regroup(selected):
    grouped = {}
    for item, bullet in selected:
      key = item.get("title") or item.get("name") or item.get("org") or "Item"
      if key not in grouped:
        grouped[key] = {**item, "bullets": []}
      grouped[key]["bullets"].append(bullet)
    return list(grouped.values())

  out["experience"] = regroup(exp_top) if experience else []
  out["projects"] = regroup(proj_top) if projects else []

  return out
