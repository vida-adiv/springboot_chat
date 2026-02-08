package com.vida.chat.models;

import jakarta.persistence.*;

@Entity
@Table(name="messages")
public class Message {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    int id;
    int recipient;
    String msg;
    protected Message() {
        // JPA needs it
    }
    public Message(int recipient, String msg){
        this.recipient = recipient;
        this.msg=msg;
    }

    public int getRecipient() {
        return recipient;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }

    public void setRecipient(int recipient) {
        this.recipient = recipient;
    }
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

}
