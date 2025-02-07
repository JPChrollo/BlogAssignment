from flask import Blueprint, render_template

@core.route("/info")
def info():
    return render_template("info.html")
