call set FLASK_APP=application.py 
call set FLASK_DEBUG=1 
call set DATABASE_URL=postgres://kzemwwjvaefepf:f9d0e705d2c357d08ccc9f90be96cba5204700df35fa6afa0bedb2c8de0e1b02@ec2-3-222-150-253.compute-1.amazonaws.com:5432/d2nr28v79kbrif
call flask run