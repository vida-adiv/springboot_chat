package com.vida.chat.service;


import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;
import io.jsonwebtoken.security.Keys;
import java.security.Key;
import java.util.Date;
import java.util.Map;

public class JwtProvider {
    @Value("${jwt.secret}")
    private String secret;

    @Value("${jwt.expirationsMs}")
    private long expirationMs;

    @Value("${jwt.issuer")
    private String issuer;

    private Key key;

    @PostConstruct
    public void init(){

        this.key=Keys.hmacShaKeyFor(secret.getBytes());
    }

    public String generateToken(Integer userId, Map<String,Object> extraClaims){
        Date now = new Date();
        Date exp = new Date(now.getTime()+ expirationMs);
        String jwt=Jwts.builder().claim("userId",userId).signWith(key, SignatureAlgorithm.HS256).compact();
        return jwt;
    }

    //todo: boolean validateJwtT(String token)
}
