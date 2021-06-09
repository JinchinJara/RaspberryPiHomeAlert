package com.example.growth4;

import java.util.Date;

public class VisitorModel {
    private String name;
    private long date;
    private String path;

    public VisitorModel(){}

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDate() {
        return new Date(date*1000).toString();
    }

    public void setDate(long date) {
        this.date = date;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }
}
