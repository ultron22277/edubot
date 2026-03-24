import json
import requests
from bs4 import BeautifulSoup

# ── All pages to scrape ──────────────────────────────────────────────────────
PAGES = {
    "faq": "https://ictkerala.org/en/faq/",
    "about": "https://ictkerala.org/en/about-us/",
    "learners": "https://ictkerala.org/en/learners/",
    "programs": "https://ictkerala.org/allprograms/",
}


def scrape_page(url):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    # Remove scripts and styles
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    # Clean up blank lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


# ── FAQ data (already collected from website) ────────────────────────────────
FAQ_DATA = [
    {
        "question": "Who can apply for the course?",
        "answer": "Graduates from Engineering/Science having a foundation level knowledge in Mathematics and Computer fundamental skills can apply. Those awaiting final results can also apply.",
    },
    {
        "question": "What is the age limit for applying?",
        "answer": "The age limit is 20 to 56 years.",
    },
    {
        "question": "What is the duration of the long term courses?",
        "answer": "6 months including internship.",
    },
    {
        "question": "Is the registration fee refundable?",
        "answer": "No, the registration fee of Rs 250 is not refundable.",
    },
    {
        "question": "Can working professionals or students join?",
        "answer": "Yes, the course is suitable for both working professionals and students awaiting final results. Recorded videos of live sessions will also be available.",
    },
    {
        "question": "Is there a scholarship scheme?",
        "answer": "Yes. Based on performance in the Entrance Test, female candidates are eligible for 100% scholarship and male candidates for 70% scholarship from KKEM.",
    },
    {
        "question": "What are the criteria for the final assessment?",
        "answer": "Candidates should have minimum 80% attendance for live sessions and must complete all assignments and assessments as per the course Quality Framework.",
    },
    {
        "question": "Can non-Keralites apply?",
        "answer": "Yes, the programme is open for anyone. However, the 75% scholarship is only for Keralites. A 25% scholarship is available for candidates from outside the state.",
    },
    {
        "question": "What subjects are covered in the Scholarship Test?",
        "answer": "It is a 60-minute online remote proctor test covering Numerical Ability, Logical Reasoning, Data Manipulation, and Verbal Ability. No negative marks.",
    },
    {
        "question": "What partner badges are provided?",
        "answer": "Microsoft and Robotic Process Automation by Automation Anywhere.",
    },
]

# ── Contact & Location data ──────────────────────────────────────────────────
CONTACT_DATA = [
    {
        "question": "What is the email address of ICT Academy of Kerala?",
        "answer": "info@ictkerala.org",
    },
    {
        "question": "What is the phone number of ICT Academy of Kerala?",
        "answer": "+91 75 940 51437",
    },
    {
        "question": "Where is the headquarters of ICT Academy of Kerala?",
        "answer": "G1, Ground Floor, Thejaswini, Technopark Campus, Thiruvananthapuram, Kerala, India – 695 581. Phone: +91 471 270 0811",
    },
    {
        "question": "Where is the Regional Centre (Central)?",
        "answer": "B-Wing, Kanikonna Villa, Infopark Campus Koratty, Thrissur, Kerala, India – 680 308. Phone: +91 480 273 1050",
    },
    {
        "question": "Where is the Regional Centre (North)?",
        "answer": "2nd Floor, UL Cyberpark Building, Nellikode Post, Kozhikode, Kerala, India – 673 016. Phone: +91 495 243 1432",
    },
    {
        "question": "How can I contact ICT Academy of Kerala?",
        "answer": "Email: info@ictkerala.org | Phone: +91 75 940 51437 | Headquarters: Technopark Campus, Thiruvananthapuram",
    },
]

# ── About data ───────────────────────────────────────────────────────────────
ABOUT_DATA = [
    {
        "question": "What is ICT Academy of Kerala?",
        "answer": "ICT Academy of Kerala (ICTAK) is the premier hub for ICT and innovation training in Kerala. Founded in 2014, it leads in skill development, technology training, and specialized project fulfilment.",
    },
    {
        "question": "When was ICT Academy of Kerala founded?",
        "answer": "ICT Academy of Kerala was founded in 2014.",
    },
    {
        "question": "What does ICT Academy of Kerala do?",
        "answer": "ICTAK offers skill development programs, technology training, industry readiness programs, upskilling programs, and connects learners with companies. It serves learners, corporates, academia, and government.",
    },
    {
        "question": "What is ICTAK TalentScout?",
        "answer": "ICTAK TalentScout is a campus drive portal that bridges the gap between fresh graduates and leading IT companies, offering opportunities and resources for career growth.",
    },
    {
        "question": "Where are ICTAK offline programs held?",
        "answer": "ICTAK offline programs are held in Kerala's IT parks for face-to-face sessions led by industry experts.",
    },
]

# ── Programs data ────────────────────────────────────────────────────────────
PROGRAMS_DATA = [
    {
        "question": "What programs does ICT Academy of Kerala offer?",
        "answer": "ICTAK offers: Industry Readiness Programs, Upskilling Programs, Essential Skill Programs, Nanoskill Programs, Partner Programs, and ASPIRE-Unnathi Programs.",
    },
    {
        "question": "What are the current courses available at ICTAK?",
        "answer": "Current courses include: Data Science & Analytics, Full Stack Developer (MERN), AI & Machine Learning, Cyber Security, Data Analysis and Visualisation, Cloud Computing, Executive Program in Advanced AIML, AWS Certified Developer, UI/UX Design in Figma, Java Programming, Flutter Developer, DevOps with Azure, Digital Marketing with AI, Business Intelligence with Power BI, Python Programming, and more.",
    },
    {
        "question": "Does ICTAK offer online programs?",
        "answer": "Yes, ICTAK offers both online (virtual classroom) and offline (physical classroom in IT parks) programs.",
    },
    {
        "question": "What certifications does ICTAK provide?",
        "answer": "ICTAK provides certifications in areas like Data Science, Cybersecurity, Software Testing, AI/ML, Full Stack Development, and more. Partner badges from Microsoft and Automation Anywhere are also provided.",
    },
    {
        "question": "How long are ICTAK programs?",
        "answer": "Long term courses are approximately 6 months including internship. Short programs vary in duration.",
    },
    {
        "question": "How can I apply for a program at ICTAK?",
        "answer": "You can apply at https://ictkerala.org/allprograms/ or visit the official website https://ictkerala.org",
    },
]

# ── Combine all data ─────────────────────────────────────────────────────────
all_data = FAQ_DATA + CONTACT_DATA + ABOUT_DATA + PROGRAMS_DATA

# ── Save as JSON ─────────────────────────────────────────────────────────────
with open("ml/data/raw/ictak_data.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(all_data)} Q&A pairs to ml/data/raw/ictak_data.json")

# ── Also scrape extra text from pages ───────────────────────────────────────
print("\nScraping pages for additional text...")
scraped = {}
for name, url in PAGES.items():
    try:
        print(f"  Scraping {name}...")
        scraped[name] = scrape_page(url)
        print(f"  ✅ {name} done")
    except Exception as e:
        print(f"  ❌ {name} failed: {e}")

with open("ml/data/raw/ictak_scraped.json", "w", encoding="utf-8") as f:
    json.dump(scraped, f, indent=2, ensure_ascii=False)

print(f"\n✅ Scraped text saved to ml/data/raw/ictak_scraped.json")
print("\n🎉 Day 2 data collection complete!")
