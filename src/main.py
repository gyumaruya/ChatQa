"""
Copyright © 2022 gyumaruya gyumaru7a@gmail.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

LICENSE_STR = """
Licensed under the Apache License, Version 2.0 (the "License");  
you may not use this file except in compliance with the License.  
You may obtain a copy of the License at  
  
    http://www.apache.org/licenses/LICENSE-2.0  
  
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
See the License for the specific language governing permissions and
limitations under the License.  
"""

COPYRIGHT_STR = """Copyright © 2022 gyumaruya gyumaru7a@gmail.com  """

GITHUB_URL="""https://github.com/gyumaruya/ChatQa"""
CHACHE_DIR = "/app/cache"

import streamlit as st
import datetime
import question_db
import pickle
import os
from streamlit_autorefresh import st_autorefresh


st.set_page_config(
    page_title="Chat Q&a",
    page_icon="❓",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": f"{GITHUB_URL}",
        "About": f"""# This is Chat Q&A: Q & A contoroller.  

- - -  
  
{COPYRIGHT_STR}
  
{LICENSE_STR}
- - -  
  
""",
    },
)

def main():
    st.session_state["ctx"] = AppContext()
    # header rendering
    left_header, right_header = st.columns([2, 1])
    left_header.write(
        """テキストベースで質問を投げましょう。  
質問は記録することができます。
"""
    )
    st.session_state["ctx"].host_mode = st.sidebar.checkbox("host mode")
    st.session_state["ctx"].getmode(right_header.empty())
    st.session_state["ctx"].save_button(st.sidebar.empty(), st.sidebar.empty())

    st.session_state["ctx"].Questions.register_user("hoge")

    # main rendring
    left, right = st.columns([2, 3])
    writer(right, st.session_state["ctx"])
    lister(left, st.session_state["ctx"])

    # footer rendering
    st.write(
        f"""- - -
Chat Q&A.  
{COPYRIGHT_STR}"""
    )


@st.cache(allow_output_mutation=True)
class AppContext:
    """Mode controle context"""

    @st.cache(allow_output_mutation=True)
    def __init__(self):
        self.debug_mode = False
        self.host_mode = False

        self.init_question()

    def set_logfile(self):
        now = datetime.datetime.now()
        self.log_file_name = os.path.join(CHACHE_DIR, f"{now.strftime('%Y%m%d_%H%M%S')}")

    def save_file(self):
        os.makedirs(CHACHE_DIR, exist_ok=True)
        with open(self.log_file_name + ".bin", "wb") as f:
            pickle.dump(self.Questions, f)

    def getmode(self, placeholder):
        if self.host_mode:
            placeholder.write("🗣 host mode")
        else:
            placeholder.write("👥 client mode")

    def init_question(self):
        self.set_logfile()
        self.Questions = question_db.QuestionDB()

    def save_question(self):
        self.save_file()
        self.init_question()

    def save_button(self, placeholder_button, placeholder_input):
        savename = placeholder_input.text_input(
            "保存ファイル名", disabled=not (self.host_mode)
        )
        self.log_file_name = os.path.join(CHACHE_DIR, savename)
        placeholder_button.button(
            "保存 & 初期化", on_click=self.save_question, disabled=not (self.host_mode)
        )


def writer(placeholder, ctx):
    """ Write panel == question Writer"""

    placeholder.header("✍ 質問をする")

    question = placeholder.text_input("文章でかく！匿名だよ！")
    if placeholder.button("投稿"):
        ctx.Questions.register_question(question, 0)


def lister(placeholder, ctx):
    """ Left panel == question list"""

    # reflesh evrytime
    st_autorefresh(interval=300, key="inf")
    placeholder.header("❓質問リスト")

    num_question = len(ctx.Questions)
    for target_hash in ctx.Questions.get_hash_sortby_lgtm():
        placeholder.write("- - -")
        desc, count = ctx.Questions.view(target_hash)
        placeholder.write(desc)
        placeholder.write("いいね数: {}".format(count))
        if placeholder.button("👍 気になる!いいね!", key=f"lgtm_{target_hash}"):
            ctx.Questions.increment(target_hash)
        if placeholder.button(
            "✅ 解決/回答済み", key=f"done_{target_hash}", disabled=not (ctx.host_mode)
        ):
            ctx.Questions.done(target_hash)


if __name__ == "__main__":
    main()
