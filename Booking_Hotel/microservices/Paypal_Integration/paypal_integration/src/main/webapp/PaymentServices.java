package com.esdg1t5;

import java.util.ArrayList;
import java.util.List;

import com.paypal.api.payments.Amount;
import com.paypal.api.payments.Details;
import com.paypal.api.payments.Item;
import com.paypal.api.payments.ItemList;
import com.paypal.api.payments.Links;
import com.paypal.api.payments.Payer;
import com.paypal.api.payments.PayerInfo;
import com.paypal.api.payments.Payment;
import com.paypal.api.payments.PaymentExecution;
import com.paypal.api.payments.RedirectUrls;
import com.paypal.api.payments.Transaction;
import com.paypal.base.rest.APIContext;
import com.paypal.base.rest.PayPalRESTException;

public class PaymentServices {
    // AZDkuMCcS70a1FFVc1NUm2rGAVUYrLAPHKYta7sL5ri8w9xI-qbM1fG8KPtd0X_UbsxiFw3Jh_pl164y -- Paypal Sandbox API Credentials (ESDG1T5) under REST APIs created.(Client_ID)
    private static final String CLIENT_ID = "AZDkuMCcS70a1FFVc1NUm2rGAVUYrLAPHKYta7sL5ri8w9xI-qbM1fG8KPtd0X_UbsxiFw3Jh_pl164y";
    // EHFubVtxUTXjDWEdg0OkpzVBRvggsmOAiv7_bcD_BQqnXKv1idPELPgK4oYl2FY54U-JTidBiAkK8jZV -- Paypal Sandbox API Credentials (ESDG1T5). (Client_Secret)
    private static final String CLIENT_SECRET = "EHFubVtxUTXjDWEdg0OkpzVBRvggsmOAiv7_bcD_BQqnXKv1idPELPgK4oYl2FY54U-JTidBiAkK8jZV";
    // Need to ensure that this is set to "sandbox"
    private static final String MODE = "sandbox";


    // Function to check for validity of payment details
    // Calls getPayerInformation(), getRedirectURLs(), and getTransactionInformation() - which return payer information, redirect URLs, and transaction info respectively.
    // Values are used to create a new payment object using the PayPal REST API
    // Finally an API context object is created with the PayPal API Credentials
    public String authorizePayment(OrderDetail orderDetail) throws PayPalRESTException {

        Payer payer = getPayerInformation();
        RedirectUrls redirectUrls = getRedirectURLs();
        List<Transaction> listTransaction = getTransactionInformation(orderDetail);

        Payment requestPayment = new Payment();
        requestPayment.setTransactions(listTransaction);
        requestPayment.setRedirectUrls(redirectUrls);
        requestPayment.setPayer(payer);
        requestPayment.setIntent("authorize");

        APIContext apiContext = new APIContext(CLIENT_ID, CLIENT_SECRET, MODE);

        Payment approvedPayment = requestPayment.create(apiContext);

        System.out.println("=== CREATED PAYMENT: ====");
		System.out.println(approvedPayment);

        return getApprovalLink(approvedPayment);
    }

    // Payer Object
    private Payer getPayerInformation() {
        // Need to specify Payer Information
        Payer payer = new Payer();
        payer.setPaymentMethod("paypal");

        PayerInfo payerInfo = new PayerInfo();
        // Set manually Sandbox's credentials
        payerInfo.setFirstName("John");
        payerInfo.setLastName("Doe");
        payerInfo.setEmail("sb-c7k1l15256719@business.example.com");
        payerInfo.setBuyerAccountNumber("K7APEFBYHBLRW");
        payerInfo.setPhone("6479955515");

        payer.setPayerInfo(payerInfo);

        return payer;
    }

    // RedirectUrls
    private RedirectUrls getRedirectURLs() {
        RedirectUrls redirectUrls = new RedirectUrls();
        // To redirect user back to store page, when they don't want to proceed with the payment.
        // Link to cancel.jsp
        redirectUrls.setCancelUrl("");
        // Link to review_payment.html
        redirectUrls.setReturnUrl("");

        return redirectUrls;
    }

    private List<Transaction> getTransactionInformation(OrderDetail orderDetail) {
		Details details = new Details();
		details.setSubtotal(orderDetail.getSubTotal());
		details.setTax(orderDetail.getTax());

		Amount amount = new Amount();
		amount.setCurrency("SGD");
		amount.setTotal(orderDetail.getTotal());
		amount.setDetails(details);

		Transaction transaction = new Transaction();
		transaction.setAmount(amount);
		transaction.setDescription(orderDetail.getRoomName());
		
		ItemList itemList = new ItemList();
		List<Item> items = new ArrayList<>();
		
		Item item = new Item();
		item.setCurrency("USD");
		item.setName(orderDetail.getRoomName());
		item.setPrice(orderDetail.getSubTotal());
		item.setTax(orderDetail.getTax());
		item.setQuantity("1");
		
		items.add(item);
		itemList.setItems(items);
		transaction.setItemList(itemList);

		List<Transaction> listTransaction = new ArrayList<>();
		listTransaction.add(transaction);	
		
		return listTransaction;
	}
	

    // takes in a payment object as a parameter and returns the approval URL associated with that payment.The function retrieves a list of links associated with the payment object using the getLinks() method. It then iterates through each link and checks if its relationship type is “approval_url”. If it is, it sets the approval link to the URL associated with that link and breaks out of the loop. Finally, it returns the approval link.
    
	private String getApprovalLink(Payment approvedPayment) {
		List<Links> links = approvedPayment.getLinks();
		String approvalLink = null;
		
		for (Links link : links) {
			if (link.getRel().equalsIgnoreCase("approval_url")) {
				approvalLink = link.getHref();
				break;
			}
		}		
		
		return approvalLink;
	}

    // Function takes in a payment ID and payer ID as parameters. It creates a new payment execution object and sets the payer ID. It then creates a new payment object with the given payment ID. An API context object is created with the PayPal API credentials. Finally it calls the execute() method on the payment object to execute the payment using the PayPal REST API. 

	public Payment executePayment(String paymentId, String payerId) throws PayPalRESTException {
		PaymentExecution paymentExecution = new PaymentExecution();
		paymentExecution.setPayerId(payerId);

		Payment payment = new Payment().setId(paymentId);

		APIContext apiContext = new APIContext(CLIENT_ID, CLIENT_SECRET, MODE);

		return payment.execute(apiContext, paymentExecution);
	}

    // The getPaymentDetails() function takes in a payment ID as a parameter. An API context object is created with the PayPal API credentials. It then retrieves details about the specified payment using the PayPal Rest API.
	
	public Payment getPaymentDetails(String paymentId) throws PayPalRESTException {
		APIContext apiContext = new APIContext(CLIENT_ID, CLIENT_SECRET, MODE);
		return Payment.get(apiContext, paymentId);
	}
}
