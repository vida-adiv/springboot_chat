package com.vida.chat.service;

import org.springframework.stereotype.Service;


import io.jsonwebtoken.*;
import io.jsonwebtoken.Jws;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;
import io.jsonwebtoken.security.Keys;

import javax.crypto.SecretKey;
import java.security.Key;
import java.util.Date;
import java.util.Map;

@Service
public class JwtProvider {
    @Value("${jwt.secret}")
    private String secret;

    @Value("${jwt.expirationsMs}")
    private long expirationMs;

    @Value("${jwt.issuer")
    private String issuer;

    private SecretKey key;

    @PostConstruct
    public void init() {
        this.key = Keys.hmacShaKeyFor(secret.getBytes());
    }

    public String generateToken(Integer userId) {
        Date now = new Date();
        Date exp = new Date(now.getTime() + expirationMs);
        String jwt = Jwts.builder().claim("userId", userId).signWith(key, SignatureAlgorithm.HS256).compact();
        return jwt;
    }

    public boolean validateJwt(String token) {
        try {
            Jws<Claims> jws = Jwts.parser().verifyWith(key).build().parseSignedClaims(token);
        } catch (Exception e) {
            System.out.println("Failed to validate token: e");
            return false;
        }
        return true;
    }
}
