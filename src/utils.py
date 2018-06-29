def pprint_message_str(message):
    return '' if message == None else '{}\n{}\n{}'.format('-' * len(message), message, '-' * len(message))

__all__ = ['pprint_message_str']
