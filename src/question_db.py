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

import hashlib
import copy
from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass
class Question:
    # main key
    hash: str = ""

    description: str = "hoge"
    user_id: int = 0
    lgtm_count: int = 0
    done: bool = False


@dataclass
class User:
    # main key
    user_id: int = 0

    name: str = "anonymous"
    description: str = "people"


class QuestionDB:
    def __init__(self):
        self.questions = dict()
        self.users = dict()

    def register_question(self, description, user_id):
        question_hs = hashlib.sha512(description.encode()).hexdigest()
        self.questions[question_hs] = Question(question_hs, description, user_id)

    def register_user(self, name, description="", user_id=None):
        # user_id:int
        if user_id is None:
            user_id = len(self.users)
        self.users[user_id] = User(user_id, name, description)
        return user_id

    def view(self, hash):
        question = self.questions[hash]
        return question.description, question.lgtm_count

    def increment(self, hash):
        self.questions[hash].lgtm_count = 1 + self.questions[hash].lgtm_count

    def done(self, hash):
        self.questions[hash].done = True

    def get_undo_questions(self):
        undo_questions = copy.deepcopy(self.questions)
        for key in list(undo_questions):
            if undo_questions[key].done:
                del undo_questions[key]

        return undo_questions

    def get_hash_sortby_lgtm(self):
        undo_questions = self.get_undo_questions()
        if 0 == len(undo_questions):
            return []
        hash_lgtm_combs = [[k, v.lgtm_count] for k, v in undo_questions.items()]
        hashs = list(map(lambda x: x[0], hash_lgtm_combs))
        lgtms = list(map(lambda x: x[1], hash_lgtm_combs))
        index_sorted_lgtm = np.argsort(hashs)
        sorted_hash = np.take(hashs, index_sorted_lgtm)
        return sorted_hash

    def get_DF(self):
        df = pd.DataFrame()

    def __len__(self):
        return len(self.get_undo_questions())
