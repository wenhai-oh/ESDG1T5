// Before payment is executed, Paypal needs to verify the details of the transaction. So we need to send the order details to PayPal server to get an approval link if the transaction information is valid.

package Booking_Hotel.microservices;
import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
 
import com.paypal.base.rest.PayPalRESTException;
 
@WebServlet("/authorize_payment")
public class AuthorizePaymentServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;
 
    public AuthorizePaymentServlet() {
    }
 
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String roomName = request.getParameter("roomName");
        String roomType = request.getParameter("roomType");
        String tax = request.getParameter("tax");
        String subtotal = request.getParameter("subtotal");
        String total = request.getParameter("total");
         
        OrderDetail orderDetail = new OrderDetail(roomName, subtotal, roomType, tax, total);
 
        try {
            PaymentServices paymentServices = new PaymentServices();
            String approvalLink = paymentServices.authorizePayment(orderDetail);
 
            response.sendRedirect(approvalLink);
             
        } catch (PayPalRESTException ex) {
            request.setAttribute("errorMessage", ex.getMessage());
            ex.printStackTrace();
            request.getRequestDispatcher("error.jsp").forward(request, response);
        }
    }
 
}

public class AuthorizePaymentServlet {
    
}
