import gradio as gr
import json
import os
import argparse


def main(self_review_number):
    DATA_FOLDER = f"self_review_{self_review_number}"
    os.makedirs(DATA_FOLDER, exist_ok=True)
    DATA_FILE = os.path.join(DATA_FOLDER, "student_data.json")

    def load_data():
        """JSON 파일에서 학생 정보를 로드하는 함수."""
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                modal_html = data.get("modal_html", "No HTML content")
                student_info = data.get("student_info", "No student info")
            return modal_html, student_info
        except FileNotFoundError:
            return "Data file not found.", "No student info"
        except json.JSONDecodeError:
            return "Invalid JSON data in the file.", "No student info"

    def submit_opinion(opinion, student_info):
        """사용자의 의견을 JSON 파일로 저장하는 함수."""
        opinion_file_path = os.path.join(DATA_FOLDER, f"{student_info}_opinion.json")
        try:
            with open(opinion_file_path, "w", encoding="utf-8") as f:
                json.dump({"opinion": opinion}, f)
            return "Opinion submitted successfully!"
        except Exception as e:
            return f"Failed to submit opinion: {e}"

    def update_interface():
        """인터페이스를 업데이트하기 위한 함수."""
        modal_html, student_info = load_data()
        return modal_html, student_info

    # Gradio 인터페이스 정의
    with gr.Blocks() as app:
        gr.Markdown("# Student Review Interface")

        # Load Data 버튼을 맨 위에 배치
        load_button = gr.Button("Load Data")

        with gr.Row():
            with gr.Column(scale=3):  # 왼쪽 열, modal_html 출력, scale=3
                modal_output = gr.HTML()
            with gr.Column(scale=1):  # 오른쪽 열, 입력과 버튼, scale=1
                opinion_input = gr.Textbox(label="Your Opinion:")
                submit_button = gr.Button("Submit Opinion")
                output_label = gr.Label()
            state = gr.State()

        # Load Data 버튼 클릭 시 modal_output과 state 업데이트
        load_button.click(fn=update_interface, outputs=[modal_output, state])

        # Submit Opinion 버튼 클릭 시 의견 제출
        submit_button.click(
            fn=submit_opinion, inputs=[opinion_input, state], outputs=output_label
        )

    app.launch()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the Gradio app with a specific review session number."
    )
    parser.add_argument(
        "self_review_number",
        type=int,
        help="The self-review session number to use for folder management.",
    )
    args = parser.parse_args()

    main(args.self_review_number)
