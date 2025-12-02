from robot import Robot

def main():
    robot = Robot()
    
    try:
        robot.run()
    finally:
        robot.cleanup()
    
if __name__ == "__main__":
    main()