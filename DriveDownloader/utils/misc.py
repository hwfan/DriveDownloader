#############################################
#  Author: Hongwei Fan                      #
#  E-mail: hwnorm@outlook.com               #
#  Homepage: https://github.com/hwfan       #
#############################################
def format_size(num_size):
    try:
        num_size = float(num_size)
        KB = num_size / 1024
    except:
        return "Error"
    if KB >= 1024:
        M = KB / 1024
        if M >= 1024:
            G = M / 1024
            return '%.3f GB' % G
        else:
            return '%.3f MB' % M
    else:
        return '%.3f KB' % KB 