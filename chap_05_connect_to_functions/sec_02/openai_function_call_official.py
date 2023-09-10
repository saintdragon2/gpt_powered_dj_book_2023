
import openai
import json

openai.api_key = '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'

# get_current_weather함수를 실제로 구현한다면, 실제 날씨 정보 API를 이용해야 하겠지만,
# 여기서는 예시를 위해 간단하게만 하드코딩 된 함수를 제공합니다. 
def get_current_weather(location, unit="fahrenheit"):
    """location으로 받은 지역의 날씨를 알려주는 기능"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

def run_conversation():
    # Step 1: messages 뿐만 아니라, 사용할 수 있는 함수에 대한 설명을 추가합니다. 
    messages = [{"role": "user", "content": "What's the weather like in Boston?"}]
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto가 기본 설정입니다. 
    )
    response_message = response["choices"][0]["message"]
    print('------------\n', response_message, '\n------------\n')
    
    # Step 2: GPT의 응답이 function을 실행해야 한다고 판단했는지 확인합니다.
    if response_message.get("function_call"):
        # Step 3: 그 함수를 실행합니다. 
        available_functions = {
            "get_current_weather": get_current_weather,
        }  # 이 예제에서는 사용 가능한 함수가 하나 뿐이지만, 여러 개를 설정할 수 있습니다. 
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = fuction_to_call(
            location=function_args.get("location"),
            unit=function_args.get("unit"),
        )

        # Step 4: 함수를 실행한 결과를 GPT에게 보내 답을 받아오기 위한 부분입니다. 
        messages.append(response_message)  # GPT의 지난 답변을 messages에 추가합니다.
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # 함수 실행 결과도 GPT messages에 추가합니다. 
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # 함수 실행결과를 GPT에 보내 새로운 답변을 받아옵니다.
        return second_response

print(run_conversation())

