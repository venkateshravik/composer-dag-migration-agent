import os
class Config:
    def __init__(self):
        self.project_id = os.getenv('project_id')
        self.generative_model = "gemini-2.5-pro"

config = Config()