# достаем refer_id из команды /start
def get_refer_id(command_args):
    try:
        return str(command_args)
    except (TypeError, ValueError):
        return None