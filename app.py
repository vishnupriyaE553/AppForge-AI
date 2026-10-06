import streamlit as st
from ai_engine import ask_gemini
from prompts import (
    UNDERSTAND_PROMPT,
    PLAN_PROMPT,
    BUILD_PROMPT,
    PREVIEW_PROMPT,
    EXPLAIN_PROMPT,
    LEARN_PROMPT
)

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="AppForge AI",
    page_icon="🚀",
    layout="wide"
)


# ---------------------------------------------------
# CUSTOM STYLING
# ---------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #0b0b0f;
    color: #ffffff;
}

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    color: #a7a7b0;
    font-size: 18px;
    margin-bottom: 30px;
}

.step-card {
    background-color: #15151c;
    border: 1px solid #292934;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 10px;
    text-align: center;
}

textarea {
    background-color: #15151c !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown(
    '<div class="main-title">🚀 AppForge AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'From app idea to understanding, planning and development — '
    'with AI as your mentor.'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------
# WORKFLOW
# ---------------------------------------------------

st.markdown("### Your Development Journey")

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

steps = [
    ("💡", "Idea"),
    ("🧠", "Understand"),
    ("📋", "Plan"),
    ("🛠", "Build"),
    ("👁", "Preview"),
    ("📖", "Explain"),
    ("🎓", "Learn")
]

for col, (icon, name) in zip(
    [col1, col2, col3, col4, col5, col6, col7],
    steps
):
    with col:
        st.markdown(
            f"""
            <div class="step-card">
                <div style="font-size:25px;">{icon}</div>
                <div>{name}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


st.divider()


# ---------------------------------------------------
# APP IDEA INPUT
# ---------------------------------------------------

st.markdown("## 💡 Start With Your App Idea")

st.write(
    "Describe what you want to build. "
    "AppForge AI will first understand your idea "
    "before creating a development plan."
)

idea = st.text_area(
    "Describe your application",
    placeholder=(
        "Example:\n"
        "Build a student attendance management app for college students. "
        "It should track subjects, present and absent classes, calculate "
        "attendance percentage and warn students when attendance falls "
        "below 75%. I am a beginner in Python."
    ),
    height=180
)


# ---------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------

if st.button(
    "🧠 Analyze My App Idea",
    type="primary",
    use_container_width=True
):

    if not idea.strip():

        st.warning("Please describe your app idea first.")

    else:

        # Save idea
        st.session_state["idea"] = idea

        # Clear previous results
        st.session_state.pop("understanding", None)
        st.session_state.pop("plan", None)
        st.session_state.pop("build", None)

        # ---------------------------------------------
        # UNDERSTAND
        # ---------------------------------------------

        with st.spinner(
            "🧠 Understanding your application..."
        ):

            try:

                understand_prompt = UNDERSTAND_PROMPT.format(
                    idea=idea
                )

                understanding = ask_gemini(
                    understand_prompt
                )

                st.session_state["understanding"] = understanding

            except Exception as e:

                st.error(
                    "Unable to analyze the idea."
                )

                st.code(str(e))


        # ---------------------------------------------
        # PLAN
        # ---------------------------------------------

        with st.spinner(
            "📋 Creating your development plan..."
        ):

            try:

                plan_prompt = PLAN_PROMPT.format(
                    idea=idea
                )

                plan = ask_gemini(
                    plan_prompt
                )

                st.session_state["plan"] = plan

            except Exception as e:

                st.error(
                    "Unable to create the development plan."
                )

                st.code(str(e))
# ---------------------------------------------------
# PROJECT SUMMARY
# ---------------------------------------------------

if "idea" in st.session_state:

    st.markdown("### 📌 Current Project")

    st.info(
        f"**App Idea:** {st.session_state['idea']}"
    )

# ---------------------------------------------------
# UNDERSTAND RESULTS
# ---------------------------------------------------

if "understanding" in st.session_state:

    st.divider()

    st.markdown("## 🧠 Understand")

    st.markdown(
        st.session_state["understanding"]
    )


# ---------------------------------------------------
# PLAN RESULTS
# ---------------------------------------------------

if "plan" in st.session_state:

    st.divider()

    st.markdown("## 📋 Plan")

    st.markdown(
        st.session_state["plan"]
    )


# ---------------------------------------------------
# BUILD SECTION
# ---------------------------------------------------

if "plan" in st.session_state:

    st.divider()

    st.markdown("## 🛠 Build Your Application")

    st.write(
        "Your idea has been understood and planned. "
        "Now let AppForge AI generate the starter implementation."
    )

    if st.button(
        "🛠 Generate Starter Application",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "🛠 AI is generating your application..."
        ):

            try:

                build_prompt = BUILD_PROMPT.format(
                    idea=st.session_state["idea"],
                    plan=st.session_state["plan"]
                )

                build_result = ask_gemini(
                    build_prompt
                )

                st.session_state["build"] = build_result

            except Exception as e:

                st.error(
                    "Unable to generate the application."
                )

                st.code(str(e))


# ---------------------------------------------------
# BUILD RESULTS
# ---------------------------------------------------

if "build" in st.session_state:

    st.divider()

    st.markdown("## 🛠 Generated Application")

    st.markdown(
        st.session_state["build"]
    )
    st.download_button(
    label="⬇️ Download Generated Specification",
    data=st.session_state["build"],
    file_name="appforge_generated_project.md",
    mime="text/markdown",
    use_container_width=True
)

# ---------------------------------------------------
# PREVIEW SECTION
# ---------------------------------------------------

if "build" in st.session_state:

    st.divider()

    st.markdown("## 👁 Live App Preview")

    st.write(
        "See how the application could look and behave "
        "before implementing the final version."
    )

    if st.button(
        "👁 Generate App Preview",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "👁 Creating your interactive preview..."
        ):

            try:

                preview_prompt = PREVIEW_PROMPT.format(
                    idea=st.session_state["idea"]
                )

                preview_result = ask_gemini(
                    preview_prompt
                )

                st.session_state["preview"] = preview_result

            except Exception as e:

                st.error(
                    "Unable to generate the preview."
                )

                st.code(str(e))


# ---------------------------------------------------
# PREVIEW DISPLAY
# ---------------------------------------------------

if "preview" in st.session_state:

    st.markdown("### 📱 Application Preview")

    preview_col1, preview_col2 = st.columns(
        [2, 1]
    )

    with preview_col1:

        st.markdown(
            """
            <div style="
                background:#15151c;
                border:1px solid #33333d;
                border-radius:16px;
                padding:25px;
                min-height:350px;
            ">

            <h2>🎓 Student Attendance</h2>

            <p style="color:#a7a7b0;">
            Attendance Dashboard
            </p>

            <hr>

            <h3>📊 Overall Attendance</h3>

            <h1>81.7%</h1>

            <br>

            <p>📘 Mathematics &nbsp;&nbsp; <b>82%</b> ✓</p>

            <p>📕 Physics &nbsp;&nbsp; <b>71%</b> ⚠️</p>

            <p>📗 Computer Science &nbsp;&nbsp; <b>92%</b> ✓</p>

            <hr>

            <p>
            ⚠️ Physics attendance is below the
            required 75%.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with preview_col2:

        st.markdown("### 🤖 AI Preview")

        st.markdown(
            st.session_state["preview"]
        )
# ---------------------------------------------------
# EXPLAIN SECTION
# ---------------------------------------------------

if "build" in st.session_state:

    st.divider()

    st.markdown("## 📖 Learn From Your Code")

    st.write(
        "Don't just generate code. Understand how it works."
    )

    if st.button(
        "📖 Explain My Generated Code",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "📖 AI is explaining your code..."
        ):

            try:

                explain_prompt = EXPLAIN_PROMPT.format(
                    idea=st.session_state["idea"],
                    code=st.session_state["build"]
                )

                explanation = ask_gemini(
                    explain_prompt
                )

                st.session_state["explanation"] = explanation

            except Exception as e:

                st.error(
                    "Unable to explain the generated code."
                )

                st.code(str(e))


# ---------------------------------------------------
# EXPLANATION DISPLAY
# ---------------------------------------------------

if "explanation" in st.session_state:

    st.markdown("### 📖 Code Explanation")

    st.markdown(
        st.session_state["explanation"]
    )
# ---------------------------------------------------
# LEARN SECTION
# ---------------------------------------------------

if "explanation" in st.session_state:

    st.divider()

    st.markdown("## 🎓 Learn & Practice")

    st.write(
        "Turn your generated application into a personalized "
        "learning journey."
    )

    if st.button(
        "🎓 Create My Learning Path",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "🎓 AI is creating your personalized learning path..."
        ):

            try:

                learn_prompt = LEARN_PROMPT.format(
                    idea=st.session_state["idea"],
                    code=st.session_state["build"]
                )

                learning_result = ask_gemini(
                    learn_prompt
                )

                st.session_state["learning"] = learning_result

            except Exception as e:

                st.error(
                    "Unable to create the learning path."
                )

                st.code(str(e))


# ---------------------------------------------------
# LEARNING RESULTS
# ---------------------------------------------------

if "learning" in st.session_state:

    st.markdown("### 🎓 Your Personalized Learning Path")

    st.markdown(
        st.session_state["learning"]
    )

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.markdown("## 🚀 AppForge AI")

    st.caption(
        "AI-powered application development mentor"
    )

    # -----------------------------------------------
    # NEW PROJECT
    # -----------------------------------------------

    if st.button(
        "🆕 New Project",
        use_container_width=True
    ):

        for key in [
            "idea",
            "understanding",
            "plan",
            "build",
            "preview",
            "explanation",
            "learning"
        ]:
            st.session_state.pop(key, None)

        st.rerun()

    # -----------------------------------------------
    # DEVELOPMENT WORKFLOW
    # -----------------------------------------------

    st.divider()

    st.markdown("### Development Workflow")

    st.markdown("""
    💡 **Idea**

    🧠 **Understand**

    📋 **Plan**

    🛠 **Build**

    👁 **Preview**

    📖 **Explain**

    🎓 **Learn**
    """)

    # -----------------------------------------------
    # POWERED BY
    # -----------------------------------------------

    st.divider()

    st.markdown("### ⚙️ Powered By")

    st.markdown("""
    **AI & Development Stack**

    🤖 **Google Gemini API**  
    Used for application understanding,
    planning, code generation, explanation
    and personalized learning.

    🐍 **Python**  
    Core programming language.

    🎈 **Streamlit**  
    Interactive web application framework.

    📦 **Google GenAI SDK**  
    Connects AppForge AI with Gemini.

    🔐 **Streamlit Secrets**  
    Secure API-key management.

    🐙 **GitHub**  
    Version control and project hosting.
    """)