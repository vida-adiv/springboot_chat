package com.vida.chat.service;

import org.springframework.stereotype.Service;

import java.security.SecureRandom;
import java.util.Base64;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class NonceService {

    private final SecureRandom rng = new SecureRandom();
    private final Map<Integer, String> nonces = new ConcurrentHashMap<>();

    /** Generate a fresh nonce and remember it for the given username */
    public String createNonce(int userId){
        byte[] bytes = new byte[32];
        rng.nextBytes(bytes);
        String nonce= Base64.getUrlEncoder().withoutPadding().encodeToString((bytes));
        nonces.put(userId,nonce);
        return nonce;
    }

    /** Retrieve and remove the stored nonce (single‑use) */
    public String consumeNonce(Integer userID, String suppliedNonce) {
        String stored = nonces.get(userID);
        if (stored != null && stored.equals(suppliedNonce)) {
            // Remove it so it cannot be replayed
            nonces.remove(userID);
            return stored;
        }
        return null;
    }
}
