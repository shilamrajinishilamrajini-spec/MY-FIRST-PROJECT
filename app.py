import streamlit as st

from resume_parser import (
    extract_text_from_pdf,
    extract_text_from_txt
)

from analyzer import analyze_jobs

from job_data import jobs


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


st.title("📄 AI Resume Analyzer & Job Recommendation System")

st.write(
    "Upload your resume and find suitable jobs using Machine Learning."
)


uploaded_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf", "txt"]
)


if uploaded_file is not None:

    if uploaded_file.name.endswith(".pdf"):

        resume_text = extract_text_from_pdf(
            uploaded_file
        )

    else:

        resume_text = extract_text_from_txt(
            uploaded_file
        )


    if not resume_text.strip():

        st.error(
            "Could not extract text from the resume."
        )

    else:

        st.success(
            "Resume uploaded successfully!"
        )


        st.subheader("📄 Resume Text")

        with st.expander("View Resume Text"):

            st.write(resume_text)


        resume_skills, results = analyze_jobs(
            resume_text,
            jobs
        )


        # -------------------------
        # Skills
        # -------------------------

        st.subheader("🛠️ Skills Detected")

        if resume_skills:

            st.write(
                ", ".join(resume_skills)
            )

        else:

            st.warning(
                "No predefined skills were detected."
            )


        # -------------------------
        # Job Recommendations
        # -------------------------

        st.subheader(
            "💼 Recommended Jobs"
        )


        for index, job in enumerate(results):

            st.markdown(
                f"### {index + 1}. {job['title']}"
            )

            st.write(
                f"**Company:** {job['company']}"
            )

            st.write(
                f"**Location:** {job['location']}"
            )

            st.progress(
                min(
                    int(job["final_score"]),
                    100
                )
            )

            st.write(
                f"**Match Score:** "
                f"{job['final_score']}%"
            )

            col1, col2 = st.columns(2)


            with col1:

                st.write(
                    "**Matched Skills:**"
                )

                if job["matched_skills"]:

                    st.write(
                        ", ".join(
                            job["matched_skills"]
                        )
                    )

                else:

                    st.write("None")


            with col2:

                st.write(
                    "**Missing Skills:**"
                )

                if job["missing_skills"]:

                    st.write(
                        ", ".join(
                            job["missing_skills"]
                        )
                    )

                else:

                    st.write("None")


            st.divider()