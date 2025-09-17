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
        if any(kw == nl for kw in norm_keywords):
            start_idx = i + 1  # start capturing after the header line
            break
    if start_idx is None:
        return ""  # no matching header found

    # find next heading index after the start
    end_idx = len(lines)
    for j in range(start_idx, len(lines)):
        if any(h == norm_lines[j] for h in norm_headings):
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


def filter_text(text): 
    lines = text.splitlines()
    lines.pop(0)
    return "\n".join(lines).strip()
    
