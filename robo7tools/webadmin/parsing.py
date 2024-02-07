from threading import Thread

thread1 = Thread(target=send_to_smb, args=(''))
thread1.start()
thread1.join()

thread1.