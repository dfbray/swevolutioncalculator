package org.swevolution.multiply;

import org.swevolution.add.Add;
import org.swevolution.subtract.Subtract;

public class Multiply {
    public static int doMultiplication(int a, int b) {
        int ret = 0, loop = b;
        while(Math.abs(loop) > 0) { //lol
            ret = Add.doAddition(ret, a);
            loop = Subtract.doSubtraction(loop, 1);
        }
        return ret;
    }
}
