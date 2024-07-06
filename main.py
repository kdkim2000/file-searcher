from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from openai import OpenAI
client = OpenAI()
# assistants = client.beta.assistants.create(
#     name ="정규식 변환기",
#     instructions ="""
#         당신은 정규식을 모르는 초보자를 위한 정규식 변환기 입니다. 
#         사용자가 원하는 정규식을 입력하면 다른 설명 없이 사용자가 요청하는 정규식만 알려 줘야 합니다. 
#         사용자가 정규식을 메시지로 받아 바로 활용해야 하기 때문입니다.
#     """,
#     tools=[{"type": "code_interpreter"}],
#     model="gpt-4o",
#     temperature=0.0,
# )
# print(assistants)
# Assistant(id='asst_z3EJn8lrcE2zBxRZWxTydCqH', created_at=1720229892, description=None, instructions='\n        당신은 정규식을 모르는 초보자를 위한 정규식 변환기 입니다. \n        사용자가 원하는 정규식을 입력하면 다른 설명 없이 사용자가 요청하는 정규식만 알려 줘야 합니다. \n        사용자가 정규식을 메시지로 받아 바로 활용해야 하기 때문입니다.\n    ', metadata={}, model='gpt-4o', name='정규식 변환기', object='assistant', tools=[CodeInterpreterTool(type='code_interpreter'), FileSearchTool(type='file_search', file_search=None)], response_format='auto', temperature=0.8, tool_resources=ToolResources(code_interpreter=ToolResourcesCodeInterpreter(file_ids=[]), file_search=ToolResourcesFileSearch(vector_store_ids=[])), top_p=1.0)
# assistants = client.beta.assistants.update(
#     assistant_id = assistant_id,
#     temperature=0.0,
#     tools=[{"type": "code_interpreter"}],
# )
#thread = client.beta.threads.create()
#print(thread)
#Thread(id='thread_Vg9QGDV8mBF7tN3QpK3Xqznz', created_at=1720248292, metadata={}, object='thread', tool_resources=ToolResources(code_interpreter=None, file_search=None))