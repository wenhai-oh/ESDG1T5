package com.esdg1t5;

public class OrderDetail{
    private String roomName;
    private float subTotal;
    private float tax;
    private float total;

    public OrderDetail(String roomName, String subTotal, String tax, String total) {
        this.roomName = roomName;
        this.subTotal = subTotal;
        this.tax = tax;
        this.total = total;
    }

    // Getters Functions for the above
    // Note that the getter methods return String for currency values because PayPal API requires the amount in String.

    public String getRoomName() {
        return roomName;
    }

    public String getSubTotal() {
        return String.format("%.2f", subTotal);
    }

    public String getTax() {
        return String.format("%.2f", tax);
    }

    public string getTotal() {
        return String.format("%.2f", total);
    }

}