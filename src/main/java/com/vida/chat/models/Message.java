package com.vida.chat.models;

import jakarta.persistence.*;

@Entity
@Table(name="messages")
public class Message {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    int id;
    int rec;
    String msg;
    protected Message() {
        // JPA needs it; leave empty or initialise defaults if you wish
    }
    public Message(int rec,String msg){
        this.rec =rec;
        this.msg=msg;
    }

    public int getRec() {
        return rec;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }

    public void setRec(int rec) {
        this.rec = rec;
    }
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

}
