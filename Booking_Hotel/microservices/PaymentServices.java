package Booking_Hotel.microservices;
 
import java.util.*;
 
import com.paypal.api.payments.*;
import com.paypal.base.rest.*;

// PaymentServices class encapsulates API calls to PayPal SDK. Acts as a medium layer between Java servlets and PayPal Server.
public class PaymentServices {
    private static final String CLIENT_ID = "AZDkuMCcS70a1FFVc1NUm2rGAVUYrLAPHKYta7sL5ri8w9xI-qbM1fG8KPtd0X_UbsxiFw3Jh_pl164y"; // 
    private static final String CLIENT_SECRET = "EHFubVtxUTXjDWEdg0OkpzVBRvggsmOAiv7_bcD_BQqnXKv1idPELPgK4oYl2FY54U-JTidBiAkK8jZV"; //
    private static final String MODE = "sandbox";
 
    public String authorizePayment(OrderDetail orderDetail)        
        throws PayPalRESTException {       
 
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
    
            return getApprovalLink(approvedPayment);
 
    }
    
    // Here, we specify first name, last name and email as the information for the payer.
    // Not really sure if we have this
    private Payer getPayerInformation() {
        Payer payer = new Payer();
        payer.setPaymentMethod("paypal");
         
        PayerInfo payerInfo = new PayerInfo();
        payerInfo.setFirstName("")
                 .setLastName("")
                 .setEmail("");
         
        payer.setPayerInfo(payerInfo);
         
        return payer;
    }

    // We need to specify two URLs to which PayPal will redirect during the checkout process. The customer will be redirected to the cancel URL if he chooses to cancel the payment (return to merchant). Or if the customer agrees to continue, he will be redirected to the return URL – which is the (Thank you??) page.
     
    private RedirectUrls getRedirectURLs() {
        RedirectUrls redirectUrls = new RedirectUrls();
        // To be filled up
        redirectUrls.setCancelUrl("");
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
        item.setCurrency("SGD");
        item.setName(orderDetail.getRoomName());
        item.setType(orderDetail.getRoomType());
        item.setPrice(orderDetail.getSubtotal());
        item.setTax(orderDetail.getTax());
        item.setQuantity("1");
         
        items.add(item);
        itemList.setItems(items);
        transaction.setItemList(itemList);
     
        List<Transaction> listTransaction = new ArrayList<>();
        listTransaction.add(transaction);  
         
        return listTransaction;
    }

    // This method parses the approved Payment object returned from PayPal to find the approval URL in JSON response. Thanks to PayPal Rest SDK
     
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

    // This method simply connects to PayPal server to get a Payment object based on the given paymentId.


    public Payment getPaymentDetails(String paymentId) throws PayPalRESTException {
        APIContext apiContext = new APIContext(CLIENT_ID, CLIENT_SECRET, MODE);
        return Payment.get(apiContext, paymentId);
    }

    public Payment executePayment(String paymentId, String payerId)
        throws PayPalRESTException {
            PaymentExecution paymentExecution = new PaymentExecution();
            paymentExecution.setPayerId(payerId);
        
            Payment payment = new Payment().setId(paymentId);
        
            APIContext apiContext = new APIContext(CLIENT_ID, CLIENT_SECRET, MODE);
        
            return payment.execute(apiContext, paymentExecution);
        }
}