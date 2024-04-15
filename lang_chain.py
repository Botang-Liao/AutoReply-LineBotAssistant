from langchain import PromptTemplate

template = """Question: {question}

Answer: """
prompt = PromptTemplate(
        template=template,
    input_variables=['question']
)

# user question
question = "Which NFL team won the Super Bowl in the 2010 season?"

import os

os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'

