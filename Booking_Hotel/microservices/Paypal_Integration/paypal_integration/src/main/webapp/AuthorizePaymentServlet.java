package net.codejava;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

import com.paypal.base.rest.PayPalRESTException;

// Handles POST requests sent to the "/authorize_payment" URL.
// The function retrieves the product name, subtotal, tax, and total from the request parameters. It then creates a new order detail object using these values. A new payment services object is created and used to authorize the payment using the PayPal REST API. If successful, it retrieves the approval link associated with this payment and redirects the user to that link.
// If there’s an error during payment authorization, it sets an error message attribute in the request and forwards it to an error page.

@WebServlet("/authorize_payment")
public class AuthorizePaymentServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;

	public AuthorizePaymentServlet() {
	}

	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		String roomName = request.getParameter("roomName");
		String subtotal = request.getParameter("subTotal");
		String tax = request.getParameter("tax");
		String total = request.getParameter("total");
		
		OrderDetail orderDetail = new OrderDetail(roomName, subtotal, tax, total);

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
