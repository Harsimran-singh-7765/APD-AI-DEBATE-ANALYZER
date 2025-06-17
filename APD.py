import sys
import pysqlite3
sys.modules["sqlite3"] = pysqlite3

import streamlit as st
import tempfile
# import whisper
from crewai import Agent, Task, Crew, LLM
from google.generativeai import configure
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
configure(api_key=os.environ["GEMINI_API_KEY"])
llm = LLM(model="gemini/gemini-1.5-flash")


st.set_page_config(page_title="🧠 APD AI Debate Analyzer", layout="centered")
st.title("🧠 Asian Parliamentary Debate Analyzer")
st.markdown("Upload or record 6 speeches for APD-style debate judging using AI.")

# --- Demo Toggle ---
use_demo = st.checkbox("🧪 Use Demo Transcripts Instead")

# --- File Upload OR Recording ---
uploaded_files = st.file_uploader("🎙️ Upload audio files (6 speakers)", accept_multiple_files=True, type=["mp3", "wav", "m4a"])

# --- DEMO TRANSCRIPTS ---
demo_transcripts = {
    "Speaker 1": """As Prime Minister, I stand to support the motion that this House would abolish alimony payments post-divorce. In modern society where we advocate gender equality, alimony perpetuates the outdated notion that women are financially dependent on men. It reinforces the patriarchal mindset that women cannot stand on their own feet. We propose instead to empower all individuals — regardless of gender — with access to state-funded upskilling programs post-divorce, especially homemakers. This is not anti-women; it’s pro-independence. Alimony is a band-aid, not a cure. Let’s end dependence, not sustain it.""",

    "Speaker 2": """As Deputy Prime Minister, I will elaborate. First, alimony is often weaponized. There are growing cases of misuse where financially stable individuals continue to receive payments just because the law mandates it. Second, the system is inherently sexist — rarely do men receive alimony even if they were homemakers. Equality is not about reversing roles but eliminating the imbalance altogether. In the UK, reforms are already considering replacing alimony with transitional support funds. We are not removing support; we are making it neutral, need-based, and temporary.""",

    "Speaker 3": """As Government Whip, I will rebut the opposition’s emotional narrative and crystallize our stance. The other side will claim that homemakers, often women, will suffer. But the real problem is that the system forces them into a passive role even after divorce. We propose active rehabilitation, not lifelong dependency. Moreover, alimony rarely reaches those who truly need it due to legal delays and manipulation. This motion is about evolution. We are not abandoning vulnerable people — we are upgrading support in a feminist framework. That’s real progress.""",

    "Speaker 4": """As Leader of Opposition, I strongly oppose this motion. Alimony exists because financial and social inequalities still persist. In India, 70% of women who divorce after being full-time homemakers find it hard to rejoin the workforce. Saying "get a job" post-divorce without structural support is cruel. The state doesn’t have adequate upskilling infra yet. Until equality is achieved in hiring, pay, and opportunity — alimony acts as a necessary bridge. To abolish it now is to abandon vulnerable individuals under the illusion of equality.""",

    "Speaker 5": """As Deputy Leader of Opposition, let me dismantle the proposal further. The proposition paints an ideal world. In reality, a homemaker in her 40s, out of the workforce for decades, cannot magically become employable. And let’s talk about power. Often, men pressure women to waive alimony for quicker divorces or custody. Removing legal protection just tips the power dynamic further against women. Even in the West, such as the U.S., reforms have been cautious and gradual — not abrupt. We need reform, not removal.""",

    "Speaker 6": """As Opposition Whip, I summarize our case. The proposition’s model is built on assumptions — state funding, neutral support, ideal feminism — none of which currently exists. They speak of abuse of alimony; we speak of the abuse that happens **without** it. Their best case is that a few misuse it. Our worst case is lifelong poverty for the vulnerable. Until we have true structural parity, alimony remains a **necessary evil**. We win this debate on **pragmatism**, **gender justice**, and **real-world empathy**."""
}

transcript_dict = {}

# # -------- Transcription --------
# if use_demo:
#     st.success("✅ Using demo transcripts")
#     transcript_dict = demo_transcripts

# elif uploaded_files and len(uploaded_files) == 6:
#     st.success("✅ 6 files uploaded successfully!")

#     st.markdown("### 🔄 Transcribing...")
#     model = whisper.load_model("base")

#     for i, audio in enumerate(uploaded_files):
#         with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
#             tmp_file.write(audio.read())
#             tmp_path = tmp_file.name
#         result = model.transcribe(tmp_path)
#         transcript_dict[f"Speaker {i+1}"] = result["text"]
#         st.markdown(f"**Speaker {i+1}:** {result['text'][:100]}...")

# -------- ANALYSIS --------
if transcript_dict:
    st.markdown("### 🧠 Analyzing with Agents...")

    agents = []
    tasks = []

    for i in range(6):
        speaker_id = f"Speaker {i+1}"
        analysis_agent = Agent(
            role=f"Speaker {i+1} Analyst",
            goal=f"Summarize key arguments, originality, clarity, and rebuttals from {speaker_id} in APD format.",
            backstory="You are a debate analyst AI trained in APD judging. Extract clear insights for scoring.",
            verbose=True,
            allow_delegation=False,
            llm=llm,
        )
        agents.append(analysis_agent)

        tasks.append(Task(
            description=f"Analyze this content from {speaker_id}: {transcript_dict[speaker_id]}",
            expected_output="A structured list of arguments, examples, rebuttals, and style comments.",
            agent=analysis_agent
        ))

    # --- Judge Agent ---
    judge = Agent(
        role="Final Adjudicator",
        goal="""
    You are to critically evaluate the overall debate in the Asian Parliamentary Debate (APD) format.
    Your primary goal is to determine which side — Government or Opposition — wins the debate based on matter (content), manner (style), and method (structure).

    As a judge, assess each speaker's:
    1. Arguments – Are they logical, impactful, and relevant?
    2. Engagement – Did they respond to opposing arguments effectively?
    3. Contribution – Did they fulfill their specific role (PM/DPM/Gov Whip or LO/DLO/Opp Whip)?
    4. Strategy – Was there role synergy and team cohesion?

    Ultimately, select a winning side based on the cumulative persuasiveness of their case and their ability to rebut the other side.
    """,
        backstory="""
    You are a National-Level APD Debate Adjudicator with over 10 years of experience judging top-tier national and international parliamentary debates.

    You have judged in major tournaments like UADC, ABP, and NEAO. Your judging style is methodical, fair, and feedback-heavy.
    You understand the core responsibilities of each role — from Prime Minister to Opposition Whip — and expect structure, depth, and clash engagement.

    You value whip speeches that summarize key clashes with clarity and fairness.
    You are particularly critical of bluff, fluff, or emotionally manipulative rhetoric unsupported by reasoning or real-world grounding.
    """,
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    final_task = Task(
        description="""
    You are provided with detailed analyses of six speakers in an Asian Parliamentary Debate.

    Your job is to:

    1. Begin by **defining the motion** and identifying **which team is Government (Speakers 1-3)** and **which is Opposition (Speakers 4-6)**.
    2. Provide a **critical, speaker-by-speaker evaluation** — analyze how well each speaker performed in their role (PM, DPM, Gov Whip, LO, DLO, Opp Whip).
    - Mention what key points they raised
    - How effectively they rebutted
    - Their structure, style, and logical coherence
    3. Evaluate the **team dynamics** — did each side build upon their teammates well? Did they engage with the other side’s core arguments?
    4. Pay special attention to the **Whip speeches (Speaker 3 and 6)** — assess how well they crystallized the debate and resolved major clashes.
    5. Conclude with a **clear verdict**:
    - Which team wins and **why** (explain in terms of content, clash, and strategy)
    - Rank the speakers (1st to 6th)
    - Mention the **Best Speaker**
    - Give **constructive feedback** for both teams in APD adjudication style

    Your tone should be objective, respectful, and detailed — as if you were delivering the adjudication at a real APD tournament.
    """,
        agent=judge,
        expected_output="""
    - Clear identification of motion, government, and opposition sides
    - Speaker-by-speaker analysis with argument summaries and role evaluation
    - Discussion of major clashes and how they were resolved
    - Comparative weighing of both teams' strengths and weaknesses
    - Final verdict with:
    - Winning team
    - Reasoning for the decision
    - Speaker rankings (1st to 6th)
    - Best speaker
    - Constructive team feedback (at least 2-3 points per team)
    """
    )


    # --- Crew Setup ---
    full_crew = Crew(
        agents=agents + [judge],
        tasks=tasks + [final_task],
        verbose=True
    )

    if st.button("🧠 Run Full Analysis"):
        with st.spinner("🧠 Thinking hard..."):
            result = full_crew.kickoff()
            st.markdown("### 🏁 Final Judgement")
            st.success(result)
else:
    st.warning("Please upload exactly 6 audio files OR enable demo mode.")
