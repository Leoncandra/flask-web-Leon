from flask import Flask, request, render_template_string, redirect
import random, string, datetime, os, hashlib, requests

app = Flask(__name__)
FILE_LOG = "riwayat.txt"

HTML = '''<!DOCTYPE html>
<html><head><title>WEB LEON</title>
<meta name=viewport content="width=device-width,initial-scale=1">
<style>
:root{--bg1:#667eea;--bg2:#764ba2;--box:#fff;--text:#333;--muted:#666;--input:#f5f5f5;--danger:#ff4d4d;--safe:#4caf50}
body.dark{--bg1:#1a1a2e;--bg2:#16213e;--box:#2a2a3e;--text:#eee;--muted:#aaa;--input:#1e1e2e}
*{box-sizing:border-box;transition:0.3s}
body{font-family:'Segoe UI',Arial;background:linear-gradient(135deg,var(--bg1) 0%,var(--bg2) 100%);display:flex;justify-content:center;align-items:flex-start;min-height:100vh;margin:0;padding:20px;color:var(--text)}
.container{width:100%;max-width:500px}
.box{background:var(--box);padding:30px;border-radius:20px;margin-bottom:20px;box-shadow:0 20px 60px rgba(0,0,0,0.3)}
h1{text-align:center;margin-top:0}
.topbar{display:flex;justify-content:space-between;margin-bottom:20px}
.btn-small{padding:8px 15px;background:var(--
