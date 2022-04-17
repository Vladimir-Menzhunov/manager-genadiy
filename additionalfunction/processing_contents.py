def processing_task(count):
    words = ['задач', 'задача', 'задачи']
    out = []
    remainder = count % 10
    if count == 0 or remainder == 0 or remainder >= 5 or count in range(11, 19):  
        st = str(count), words[0]
    elif remainder == 1:  
        st = str(count), words[1]      
    else:  
        st = str(count), words[2]
    out.append(" ".join(st))

    return " ".join(out)