import requests
server = "http://127.0.0.1:5700"
#/get_login_info 获取登录号信息
def get_login_info():
    url = server + "/get_login_info"
    return requests.get(url).json()

#获取群信息
def get_group_info(group_id):
    url = server + "/get_group_info"
    params = {
        "group_id": group_id
    }
    return requests.get(url, params=params).json()

#发送消息/send_msg
def send_msg(group_id, message):
    url = server + "/send_msg"
    params = {
        "group_id": group_id,
        "message": message
    }
    return requests.get(url, params=params).json()
#获取群消息历史记录/get_group_msg_history
def get_group_msg_history(group_id, message_seq):
    url = server + "/get_group_msg_history"
    params = {
        "group_id": group_id,
        "message_seq": message_seq
    }
    return requests.get(url, params=params).json()

#获取消息/get_msg
def get_msg(message_id):
    url = server + "/get_msg"
    return requests.get(url).json()

def get_grop_member_list(grop_id):
    """获取群成员列表"""
    url = server + "/get_group_member_list"
    return requests.get(url).json()
def get_group_member_info(groupid,userid):
    """获取群成员信息"""
    #/get_group_member_info
    url = server + "/get_group_member_info"
    params = {
        "group_id": groupid,
        "user_id": userid
    }
    return requests.get(url, params=params).json()