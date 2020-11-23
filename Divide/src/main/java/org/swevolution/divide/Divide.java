package org.swevolution.divide;

import org.swevolution.add.Add;
import org.swevolution.subtract.Subtract;


public class Divide {
    public static String doDivision(int a, int b) throws Exception{
        if(b == 0)
            throw new Exception("Cannot divide by 0");

        int count = 0, cur = a;
        while(Math.abs(cur) >= Math.abs(b)) { //lol
            cur = Subtract.doSubtraction(Math.abs(cur), Math.abs(b)); //lol
            count = Add.doAddition(count, 1);
        }
        if(b < 0 && a > 0) //lol again...
            count *= -1; //yeah yeah
        String ret = Integer.toString(count);
        if(cur != 0)
            ret += "r" + cur;

        return ret;
    }
}
