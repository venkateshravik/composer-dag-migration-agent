import os
class Config:
    def __init__(self):
        self.project_id = os.getenv('project_id')
        self.root_agent_model = "gemini-2.5-flash"
        self.generative_model = "gemini-2.5-pro"


config = Config()