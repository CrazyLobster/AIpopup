import anthropic

# 初始化客户端
client = anthropic.Client("your-api-key")

# 发送消息
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",  # 选择模型版本
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "你好,Claude!"
    }]
)

# 获取响应
print(message.content)