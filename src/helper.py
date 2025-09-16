description = "About the job\nAre you passionate about coding and eager to work on cutting-edge projects?\n\nA US-based client is looking for experienced developers with strong JavaScript or TypeScript skills to join their dynamic team. This role offers the opportunity to collaborate with global companies on AI-driven solutions, tackle complex challenges, and continuously enhance your skills in a fast-paced environment.\n\nWhat You\u2019ll Do\n\nWrite clean, reusable, and maintainable code.\nParticipate in code reviews to ensure high-quality standards.\nDevelop scalable, modular web applications with a focus on security and stability.\nCollaborate with teams to build advanced AI-driven solutions.\nDeliver well-structured and documented code.\n\nWhat We\u2019re Looking For\n\nOpen to applicants of all levels, from junior to industry experts.\nBachelor\u2019s or Master\u2019s degree in Computer Science, Engineering, or equivalent experience.\nStrong understanding of ES6 and frameworks like Node.js or React.\nKnowledge of front-end, back-end, or full-stack development.\nInterest in building scalable, secure web applications with clean architecture.\nGood spoken and written communication skills in English.\n\nNice To Have\n\nFamiliarity with additional frameworks like Vue.js, Angular, or Nest.js.\nUnderstanding of software quality assurance and test planning.\n\nWhat We Offer\n\nWork with leading experts worldwide and expand your professional network.\nThis is a contractual remote work opportunity without traditional job constraints.\nCompetitive salary based on global industry standards.\nExposure to innovative projects at the forefront of technology.\n\nInterview Process\n\nShortlisted developers may be asked to complete an assessment.\nIf you clear the assessment, you will be contacted for contract assignments with expected start dates, durations, and end dates.\nSome contract assignments require fixed weekly hours, averaging 20/30/40 hours per week for the duration of the contract assignment.\nnice to have"


import unicodedata
import re

# Common headings to detect (normalized)
COMMON_HEADINGS = [
    "about the job",
    "what you'll do",
    "what you will do",
    "what we are looking for",
    "what we're looking for",
    "responsibilities",
    "roles",
    "requirements",
    "qualifications",
    "skills",
    "nice to have",
    "what we offer",
    "benefits",
    "interview process",
    "how to apply",
    "job description",
]


def _normalize(s: str) -> str:
    """Normalize unicode quotes/dashes and lowercase for matching."""
    if s is None:
        return ""
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    s = unicodedata.normalize("NFKC", s)
    return s.lower().strip()


def _clean_bullets_block(text_block: str) -> str:
    """Optional: normalize bullet markers and remove leading bullet characters."""
    lines = []
    for line in text_block.splitlines():
        l = line.strip()
        # remove common bullet emojis/symbols at start (✅, •, -, *, 🔹, etc.)
        l = re.sub(
            r"^[\s\-\*\u2022\u25E6\u25AA\u25AB\u25CF\u25CB\u2713\u2714\uf0b7\u2756\u1F539\u1F53A]+",
            "",
            l,
        )
        # collapse multiple spaces
        l = re.sub(r"\s+", " ", l)
        if l:
            lines.append(l)
    return "\n".join(lines)


def extract_section(text: str, keywords, all_headings=None, clean_bullets=True) -> str:
    """
    Extract the section that starts with any of the `keywords` and ends before the next heading.
    - `text`: full job description string
    - `keywords`: list of strings to search for (e.g. ["responsibilities", "what you'll do"])
    - returns: string (empty if not found)
    """
    if all_headings is None:
        all_headings = COMMON_HEADINGS

    lines = text.splitlines()
    norm_lines = [_normalize(l) for l in lines]
    norm_keywords = [_normalize(k) for k in keywords]
    norm_headings = [_normalize(h) for h in all_headings]

    # find header index
    start_idx = None
    for i, nl in enumerate(norm_lines):
        if any(kw in nl for kw in norm_keywords):
            start_idx = i + 1  # start capturing after the header line
            break
    if start_idx is None:
        return ""  # no matching header found

    # find next heading index after the start
    end_idx = len(lines)
    for j in range(start_idx, len(lines)):
        found_heading = False
        for h in norm_headings:
            if h in norm_lines[j]:
                found_heading = True
                break
    
        if found_heading:
            end_idx = j
            break

    # collect non-empty lines between start_idx and end_idx
    block_lines = [
        lines[k].strip() for k in range(start_idx, end_idx) if lines[k].strip()
    ]
    block_text = "\n".join(block_lines).strip()

    if clean_bullets:
        block_text = _clean_bullets_block(block_text)

    return block_text


responsibilities = extract_section(
    description, ["responsibilities", "what you'll do", "what you will do", "roles"]
)
print(responsibilities)