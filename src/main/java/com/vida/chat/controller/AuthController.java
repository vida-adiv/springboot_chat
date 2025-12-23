package com.vida.chat.controller;

import com.vida.chat.models.User;
import com.vida.chat.repository.UserRepository;
import com.vida.chat.service.NonceService;
import com.vida.chat.models.TokenRequest;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.bouncycastle.util.io.pem.PemReader;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.StringReader;
import java.security.KeyFactory;
import java.security.PublicKey;
import java.security.Signature;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;
import java.util.Collections;
import java.util.Map;
import java.util.Optional;


@RestController
@RequestMapping("/auth")
public class AuthController {
    @Autowired
    private UserRepository userRepository;

    @Autowired
    private NonceService nonceService;


    @GetMapping("/nonce/{id}")
    public ResponseEntity<Map<String,String>> getNonce(@PathVariable int id){
        if(!userRepository.existsById(id)){
            return ResponseEntity.badRequest().body(Collections.singletonMap("error","unknown id"));
        }else{

            String nonce = nonceService.createNonce(id);
            return ResponseEntity.ok(Collections.singletonMap("nonce",nonce));
        }
    }


    @PostMapping("/token")
    public ResponseEntity<?> verify(@RequestBody TokenRequest request){
        if (!userRepository.existsById(request.getUserId())){
            return ResponseEntity.badRequest().body("not found");
        }
        String storedNonce =nonceService.consumeNonce(request.getUserId(), request.getNonce());
        if (storedNonce == null) {
            return ResponseEntity.badRequest()
                    .body(Collections.singletonMap("error", "invalid or expired nonce"));
        }

        // Implement verifying signature
        int userId=request.getUserId();
        Optional<User> user_op=userRepository.findById(userId);
        if(user_op.isEmpty()){
            return ResponseEntity.badRequest().body("user not found");
        }
        User user=user_op.get();
        try{
            PublicKey pubKey = loadPublicKeyFromPem(user.getPublicKey());
            verifySignature(pubKey,request.getNonce(),request.getSignature());
            return ResponseEntity.ok(Collections.singletonMap("accessToken","1234lala"));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e);
        }


        //return ResponseEntity.badRequest().body("todo");
    }

    private PublicKey loadPublicKeyFromPem(String pem) throws Exception {
        try (PemReader reader = new PemReader(new StringReader(pem))) {
            byte[] content = reader.readPemObject().getContent();
            X509EncodedKeySpec spec = new X509EncodedKeySpec(content);
            // Detect RSA vs EC by key size / algorithm name
            try {
                return KeyFactory.getInstance("RSA").generatePublic(spec);
            } catch (InvalidKeySpecException ignored) {
                // Try EC
                return KeyFactory.getInstance("EC").generatePublic(spec);
            }
        }
    }
    private static boolean verifySignature(PublicKey key,
                                           String nonceBase64,
                                           String signatureBase64) {
        try {
            // 1️⃣ Decode the incoming Base64‑URL strings
            byte[] data = Base64.getUrlDecoder().decode(nonceBase64);
            byte[] sig  = Base64.getUrlDecoder().decode(signatureBase64);

            // 2️⃣ Choose the JCA algorithm name based on the key type
            String algo;
            switch (key.getAlgorithm().toUpperCase()) {
                case "RSA":
                    algo = "SHA256withRSA";
                    break;
                case "EC":
                    algo = "SHA256withECDSA";
                    break;
                default:
                    throw new IllegalArgumentException(
                            "Unsupported key algorithm: " + key.getAlgorithm());
            }

            // Initialise the Signature verifier and perform verification
            Signature verifier = Signature.getInstance(algo);
            verifier.initVerify(key);
            verifier.update(data);
            return verifier.verify(sig);
        } catch (Exception e) {
            // Wrap any checked exception (NoSuchAlgorithmException,
            // InvalidKeyException, SignatureException, IllegalArgumentException, …)
            // into a runtime exception so the caller gets a clear failure reason.
            throw new RuntimeException("Signature verification failed", e);
        }
    }

}
