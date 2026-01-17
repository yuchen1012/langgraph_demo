from typing import TypedDict, Literal

from langchain_core.output_parsers import StrOutputParser
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from pydantic import BaseModel, Field

from agent.my_llm import llm
from agent.tools.tool_demo5 import chain


class State(TypedDict):
    joke: str  # 生成笑话的内容
    topic: str  # 用户指定的topic
    feedback: str  # 改进建议
    funny_level: str  # 笑话的评级


class Feedback(BaseModel):
    """使用此工具来结构化响应"""
    grade: Literal["funny", "not funny"] = Field(
        description="判断笑话是否幽默",
        examples=["funny", "not funny"]
    )
    feedback: str = Field(
        description="如果不幽默，提供改进建议",
        examples=["可以加入双关语或者意外结局"]
    )


# node
def generator_func(state: State):
    """由大模型生成冷笑话的节点"""
    prompt = (
        f"根据反馈的建议来改进笑话：{state['feedback']};主题：{state['topic']};"
        if state.get("feedback", None)
        else f"创建一个关于{state['topic']}的冷笑话")
    # resp = llm.invoke(prompt)
    # return {'joke': resp.content}
    chain = llm | StrOutputParser()
    resp = chain.invoke(prompt)
    return {'joke': resp}


# node
def evaluator_func(state: State):
    """评估生成的冷笑话"""
    # chain = llm.with_structured_output(Feedback)
    # resp = chain.invoke(
    #     f"评估此笑话的幽默程度:{state["joke"]}"
    #     "注意：幽默应包含意外性或巧妙措辞"
    # )
    # return {'feedback': resp.feedback, "funny_level": resp.grad}

    chain = llm.bind_tools([Feedback])
    resp = chain.invoke(
        f"评估此笑话的幽默程度:{state["joke"]}"
        "注意：幽默应包含意外性或巧妙措辞"
    )
    evaluation =  resp.tool_calls[-1]['args']
    return {
        'funny_level': evaluation['grade'],
        'feedback': evaluation['feedback']
    }

def route_func(state: State) -> str:
    """动态路由决策函数"""
    return (
        "Accept" if state.get('funny_level', 'not funny') == 'funny' else 'Reject'
    )

builder = StateGraph(State)

builder.add_node('generator', generator_func)
builder.add_node('evaluation', evaluator_func)

builder.add_edge(START, 'generator')
builder.add_edge('generator', 'evaluation')
builder.add_conditional_edges(
    'evaluation', route_func, {'Accept': END, 'Reject': 'generator'}
)

graph = builder.compile()
