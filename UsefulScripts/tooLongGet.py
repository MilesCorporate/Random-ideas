import requests
import sys


def test_get_length_limit(base_url="https://httpbin.org/get",
                          start_len=100,
                          step=100,
                          max_attempts=500):
  """
    逐步增加GET请求的URL长度，直到服务器返回414或超时。
    
    参数:
        base_url: 目标服务器地址（使用公共测试服务 httpbin.org）
        start_len: 初始参数长度
        step:     每次增加的字符数
        max_attempts: 最大尝试次数，防止无限循环
    """
  param_base = "a" * start_len
  total_len = len(base_url) + len("?test=") + start_len  # 初始总长度

  for i in range(max_attempts):
    # 构造URL：base_url?test=aaaa...
    params = "a" * (start_len + i * step)
    url = f"{base_url}?test={params}"
    current_len = len(url)

    try:
      # 发送GET请求，设置超时10秒
      resp = requests.get(url, timeout=10)
      status = resp.status_code
      print(f"尝试 {i+1}: URL长度 = {current_len:6d}, 状态码 = {status}")

      # 如果服务器返回414，说明已经达到限制
      if status == 414:
        print(f"\n✅ 达到服务器限制！最大可接受URL长度约为 {current_len - step} 个字符。")
        break

    except requests.exceptions.RequestException as e:
      # 网络异常（超时、连接错误等）也视为无法继续
      print(f"\n❌ 请求失败: {e}")
      print(f"最后成功的URL长度约为 {current_len - step} 个字符。")
      break
  else:
    print("\n⚠️ 已达到最大尝试次数，未触发限制。可以增加 max_attempts 或步长继续测试。")


if __name__ == "__main__":
  test_get_length_limit()
