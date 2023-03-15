package booking_hotel.microservices;
// Error occurs because does not match file directory 
// Not sure how to fix the above.

public class OrderDetails {
    private String roomName;
    private String roomType;
    private float subtotal;
    private float tax;
    private float total;

    public OrderDetails(String roomName, String roomType, String subtotal, String tax, String total) {
        this.roomName = roomName;
        this.roomType = roomType;
        this.subtotal = Float.parseFloat(subtotal);
        this.tax = Float.parseFloat(tax);
        this.total = Float.parseFloat(total);
    }

    public String getRoomName(){
        return roomName;
    }

    public String getRoomType(){
        return roomType;
    }

    public String getSubTotal() {
        return String.format("%.2f", subtotal);
    }

    public String getTax() {
        return String.format("%.2f", tax);
    }

    public String getTotal() {
        return String.format("%.2f", total);
    }
}