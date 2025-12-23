package com.vida.chat.models

import org.bouncycastle.crypto.Signer

data class TokenRequest(
    val userId: Integer,
    val nonce:String,
    val signature:String)
