import org.swevolution.add.Add;
import org.swevolution.subtract.Subtract;
import org.swevolution.multiply.Multiply;
import org.swevolution.divide.Divide;

public class Calculator {
    public static void main(String[] args) {
        System.out.println("Correct answer is 7, our add answer is " + Add.doAddition(4, 3));
        System.out.println("Correct answer is 1, our subtract answer is " + Subtract.doSubtraction(4, 3));

        System.out.println("Correct answer is 12, our multiply answer is " + Multiply.doMultiplication(4, 3));
        System.out.println("Correct answer is 0, our multiply answer is " + Multiply.doMultiplication(0, 0));
        System.out.println("Correct answer is -2, our multiply answer is " + Multiply.doMultiplication(2, -1));
        System.out.println("Correct answer is -2, our multiply answer is " + Multiply.doMultiplication(-2, 1));
        System.out.println("Correct answer is 2, our multiply answer is " + Multiply.doMultiplication(-2, -1));
		System.out.println("bazel!");
        try {
            System.out.println("Correct answer is 1r1, our divide answer is " + Divide.doDivision(4, 3));
            System.out.println("Correct answer is -20, our divide answer is " + Divide.doDivision(60, -3));
            System.out.println("Correct answer is 0r-3, our divide answer is " + Divide.doDivision(-3, 6));
            System.out.println("Correct answer is 1, our divide answer is " + Divide.doDivision(-3, -3));
            System.out.println("Correct answer is Exception, our divide answer is " + Divide.doDivision(4, 0));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
