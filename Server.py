#Practical No:1:

#A) Develop a client-server application using TCP in which the client sends an integer to the server and the server determines whether the number is prime and sends the results back to the client.

# server.py

import socket
HOST="127.0.0.1"
PORT=5000
def is_prime(number):
    if number<2:
        return False
    for i in range(2,int(number**0.5)+1):
        if number%i==0:
            return False
    return True
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((HOST,PORT))
server_socket.listen(1)
print("TCP prime server")
print(f"Server listening on {HOST}:{PORT}")
print("Waiting for client....")
client_socket,client_address=server_socket.accept()
print("Client connected:",client_address)
while True:
    data=client_socket.recv(1024).decode()
    if not data:
        break
    if data.lower()=="exit":
        break
    try:
        number=int(data)
        if is_prime(number):
            result=f"{number} is a PRIME number."
        else:
            result=f"{number} is NOT a PRIME number."
    except ValueError:
        result="Invalid input.Please enter an integer."
    client_socket.send(result.encode())
client_socket.close()
server_socket.close()
print("Conection closed.")

# Client.py

import socket
HOST="127.0.0.1"
PORT=5000
client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))
print("Connected to TCP Prime Server")
print("Enter an integer or type 'exit' to close")
while True:
    number=input("Enter number:")
    client_socket.send(number.encode())
    if number.lower()=="exit":
        break
    response=client_socket.recv(1024).decode()
    print("Server:",response)
client_socket.close()
print("Connection closed.")

#B) Develop a client-server TCP-based chatting application in which the client and server exchange messages until either side sends an exit.

# Server_chat.py

import socket
HOST="127.0.0.1"
PORT=5001
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((HOST,PORT))
server_socket.listen(1)
print("TCP chat server")
print("Waiting for client...")
client_socket,client_address=server_socket.accept()
print("Client connected:",client_address)
print("Type 'ext' to end the chat.")
while True:
    message=client_socket.recv(1024).decode()
    if not message:
        break
    if message.lower()=="exit":
        print("Client ended the chat.")
        break
    print("Client:",message)
    reply=input("Server:")
    client_socket.send(reply.encode())
    if reply.lower()=="exit":
        break
client_socket.close()
server_socket.close()
print("Chat connection closed")

# Client_chat.py

import socket
HOST="127.0.0.1"
PORT=5001
client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))
print("conected to TCP Chat Server")
print("Type 'exit' to end the chat")
while True:
    message=input("Client:")
    client_socket.send(message.encode())
    if message.lower()=="exit":
        break
    response=client_socket.recv(1024).decode()
    print("Server:",response)
    if response.lower()=="exit":
        break
client_socket.close()
print("Chat connection closed")

# Practical No:2:

# A) Develop a UDP based client-server application in which the client sends the name of a network service to the server and the server returns the corresponding service information.

# udp_server.py

import socket
HOST = "127.0.0.1"
PORT = 5002
services = {
    "DNS": {
        "name": "Domain name system",
        "port": "53",
        "protocol": "UDP/TCP",
        "purpose": "Translate domain name into IP addresses."
    },
    "DHCP": {
        "name": "Dynamic Host Configuration protocol",
        "port": "67/68",
        "protocol": "UDP",
        "purpose": "Automatically IP addresses and network configuration."
    },
    "HTTP": {
        "name": "Hypertext transfer protocol",
        "port": "80",
        "protocol": "TCP",
        "purpose": "Transfer web pages and web resources."
    },
    "HTTPS": {
        "name": "Hypertext transfer protocol secure",
        "port": "443",
        "protocol": "TCP",
        "purpose": "Provides secure and encrypted web communication."
    },
    "SSH": {
        "name": "Secure Shell",
        "port": "22",
        "protocol": "TCP",
        "purpose": "Provides secure remote access to computers and servers."
    },
    "NTP": {
        "name": "Network Time Protocol",
        "port": "123",
        "protocol": "UDP",
        "purpose": "Synchronizes the time of computers and network devices."
    }
}
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))
while True:
    data, client_address = server_socket.recvfrom(1024)
    request = data.decode().strip()
    service_name = request.upper()
    if service_name in services:
        service = services[service_name]
        response = (
            f"Service Name:{service['name']}\n"
            f"Default port:{service['port']}\n"
            f"Transport protocol:{service['protocol']}\n"
            f"Purpose:{service['purpose']}\n"
        )
    else:
        response = "Service not found."
    server_socket.sendto(response.encode(), client_address)

# udp_client.py

import socket
HOST = "127.0.0.1"
PORT = 5002
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    service_name = input("Enter service name: ").strip()
    if service_name.lower() == "exit":
        break
    client_socket.sendto(service_name.encode(), (HOST, PORT))
    response, server_address = client_socket.recvfrom(2048)
    print(response.decode())
client_socket.close()

# B) Develop a UDP-based client-server application that simulates an IoT temperature monitoring system in which the client sends temperature readings to the server and the server analyzes the reading and sends an appropriate status or alert back to the client.

# sensor_server.py

import socket
HOST = "127.0.0.1"
PORT = 5003
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))
while True:
    data, client_address = server_socket.recvfrom(1024)
    message = data.decode().strip()
    try:
        temperature = float(message)
        if temperature < 0:
            status = "ALERT: Extremely Low Temperature"
        elif temperature < 15:
            status = "LOW Temperature"
        elif temperature <= 35:
            status = "NORMAL Temperature"
        elif temperature <= 45:
            status = "WARNING: High Temperature"
        else:
            status = "CRITICAL: Immediate Attention Required"
    except ValueError:
        status = "Invalid temperature value."
    server_socket.sendto(status.encode(), client_address)

# sensor_client.py

import socket
HOST = "127.0.0.1"
PORT = 5003
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    temperature = input("Enter temperature in C: ").strip()
    if temperature.lower() == "exit":
        break
    client_socket.sendto(temperature.encode(), (HOST, PORT))
    response, server_address = client_socket.recvfrom(1024)
    print("Server Status:", response.decode())
client_socket.close()

# Practical No:3:

# A) Develop a student management REST API using Flask and perform complete CRUD operation using GET, POST, PUT and DELETE methods. Test the API using Thunder Client.

# Install:
# python -m pip install flask

# student_crud_api.py

from flask import Flask, jsonify, request
app = Flask(__name__)
students = [
    {"id": 1, "name": "Aditya sharma", "course": "MSc IT"},
    {"id": 2, "name": "Nidhi Tiwari", "course": "MSc IT"},
    {"id": 3, "name": "Suraj Thakur", "course": "MSc IT"}
]
@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(students)
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    for student in students:
        if student["id"] == student_id:
            return jsonify(student)
    return jsonify({"message": "Student not found"}), 404
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()
    new_student = {
        "id": data["id"],
        "namee": data["name"],
        "course": data["course"]
    }
    students.append(new_student)
    return jsonify({
        "message": "Student added successfully",
        "student": new_student
    }), 201
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json()
    for student in students:
        if student["id"] == student_id:
            student["name"] = data["name"]
            student["course"] = data["course"]
            return jsonify({
                "message": "Student updated successfully",
                "student": student
            })
    return jsonify({"message": "Student not found"}), 404
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return jsonify({"message": "Student deleted suceessfully"})
    return jsonify({"message": "Student not found"}), 404
if __name__ == "__main__":
    app.run(debug=True)

# Practical No:4:

# A) Develop a task management REST API using FastAPI and perform complete CRUD operation using GET, POST, PUT and DELETE methods. Test the API using Uvicorn.

# Install:
# python -m pip install fastapi uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI(title="Task Management API")
class Task(BaseModel):
    id: int
    title: str
    status: str
    priority: str
tasks = [
    {
        "id": 1,
        "title": "Complete Cloud Computing Assignment",
        "status": "Pending",
        "priority": "High"
    },
    {
        "id": 2,
        "title": "Prepare REST API practical",
        "status": "In Progress",
        "priority": "Medium"
    }
]
@app.get("/tasks")
def get_tasks():
    return tasks
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")
@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task.model_dump())
    return {
        "message": "Task created successfully",
        "task": task
    }
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks[index] = updated_task.model_dump()
            return {
                "message": "Task updated successfully",
                "task": updated_task
            }
    raise HTTPException(status_code=404, detail="Task not found")
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")

# Practical No:5:

# A) Understand how a TCP server handles multiple clients simultaneously using socket programming and multithreading.

# multi_service_server.py

import socket
import threading
HOST = "127.0.0.1"
PORT = 5003
def process_request(request):
    try:
        operation, value = request.split("|", 1)
        if operation == "1":
            number = int(value)
            result = 1
            for i in range(1, number + 1):
                result *= i
            return f"Factorial of {number} is {result}"
        elif operation == "2":
            number = int(value)
            fibonacci = []
            a = 0
            b = 1
            for i in range(number):
                fibonacci.append(a)
                a, b = b, a + b
            return "Fibonacci Series: " + str(fibonacci)
        elif operation == "3":
            return "Reversed Text: " + value[::-1]
        elif operation == "4":
            return f"Number of Words: {len(value.split())}"
        else:
            return "Invalid Operation"
    except Exception as error:
        return "Error: " + str(error)
def handle_client(client_socket, client_address):
    print("Client Connected:", client_address)
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data or data.lower() == "exit":
                break
            result = process_request(data)
            client_socket.send(result.encode())
        except:
            break
    client_socket.close()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(
        target=handle_client,
        args=(client_socket, client_address)
    )
    client_thread.start()

# multi_service_client.py

import socket
HOST = "127.0.0.1"
PORT = 5003
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
while True:
    operation = input("Select Operation: ")
    if operation.lower() == "exit":
        client_socket.send("exit".encode())
        break
    if operation == "1":
        value = input("Enter a number: ")
    elif operation == "2":
        value = input("Enter number of terms: ")
    elif operation == "3":
        value = input("Enter text: ")
    elif operation == "4":
        value = input("Enter text: ")
    else:
        print("Invalid operation")
        continue
    request = operation + "|" + value
    client_socket.send(request.encode())
    response = client_socket.recv(1024).decode()
    print("Server Response:", response)
client_socket.close()

# Practical No:6:

# A) Simulate a cloud environment with virtual machines and tasks, implement scheduling strategies, and compare their performance.

# Install:
# pip install tabulate

# cloud_resource_allocation.py

from tabulate import tabulate
vms = [
    {"name": "VM1", "mips": 500},
    {"name": "VM2", "mips": 1000},
    {"name": "VM3", "mips": 1500}
]
tasks = [
    {"name": "Task1", "length": 10000},
    {"name": "Task2", "length": 20000},
    {"name": "Task3", "length": 30000},
    {"name": "Task4", "length": 40000},
    {"name": "Task5", "length": 50000}
]
results = []
for i, task in enumerate(tasks):
    vm = vms[i % len(vms)]
    execution_time = task["length"] / vm["mips"]
    results.append([
        task["name"],
        task["length"],
        vm["name"],
        vm["mips"],
        round(execution_time, 2)
    ])
print(tabulate(
    results,
    headers=["Task", "Workload (MI)", "VM", "VM Capacity (MIPS)", "Execution Time"],
    tablefmt="grid"
))

# scheduling_comparison.py

from tabulate import tabulate
vms = [
    {"name": "VM1", "mips": 500},
    {"name": "VM2", "mips": 1000},
    {"name": "VM3", "mips": 1500}
]
tasks = [
    {"name": "Task1", "length": 60000},
    {"name": "Task2", "length": 10000},
    {"name": "Task3", "length": 10000},
    {"name": "Task4", "length": 60000},
    {"name": "Task5", "length": 10000}
]
def round_robin(tasks, vms):
    loads = [0] * len(vms)
    results = []
    for i, task in enumerate(tasks):
        vm_index = i % len(vms)
        vm = vms[vm_index]
        start_time = loads[vm_index] / vm["mips"]
        execution_time = task["length"] / vm["mips"]
        finish_time = start_time + execution_time
        loads[vm_index] += task["length"]
        results.append([
            task["name"],
            vm["name"],
            round(start_time, 2),
            round(execution_time, 2),
            round(finish_time, 2)
        ])
    return results
def least_loaded(tasks, vms):
    loads = [0] * len(vms)
    results = []
    for task in tasks:
        vm_index = min(
            range(len(vms)),
            key=lambda i: loads[i] / vms[i]["mips"]
        )
        vm = vms[vm_index]
        start_time = loads[vm_index] / vm["mips"]
        execution_time = task["length"] / vm["mips"]
        finish_time = start_time + execution_time
        loads[vm_index] += task["length"]
        results.append([
            task["name"],
            vm["name"],
            round(start_time, 2),
            round(execution_time, 2),
            round(finish_time, 2)
        ])
    return results
rr_results = round_robin(tasks, vms)
ll_results = least_loaded(tasks, vms)
rr_makespan = max(row[4] for row in rr_results)
ll_makespan = max(row[4] for row in ll_results)
print(tabulate(
    [["Round Robin", rr_makespan], ["Least-Loaded", ll_makespan]],
    headers=["Scheduling Method", "Total Completion Time"],
    tablefmt="grid"
))
improvement = ((rr_makespan - ll_makespan) / rr_makespan) * 100
print(f"Performance Improvement: {improvement:.2f}%")

# Practical No:7:

# A) Develop a python based interactive dashboard monitor simulated cloud resource, allocate computational tasks using different scheduling algorithms and visualize resource and task performance.

# Install:
# pip install streamlit pandas plotly

import streamlit as st
import pandas as pd
import plotly.express as px
st.title("Cloud Resource Monitoring Dashboard")
vms = pd.DataFrame({
    "VM": ["VM-1", "VM-2", "VM-3"],
    "CPU": [42, 68, 91],
    "Memory": [48, 72, 88],
    "MIPS": [500, 1000, 1500]
})
tasks = pd.DataFrame({
    "Task": ["T1", "T2", "T3", "T4", "T5", "T6"],
    "Workload": [10000, 20000, 15000, 30000, 12000, 25000],
    "Priority": ["Low", "High", "Medium", "Critical", "Low", "High"]
})
st.subheader("Cloud Resources")
st.dataframe(vms, hide_index=True)
st.plotly_chart(
    px.bar(
        vms,
        x="VM",
        y=["CPU", "Memory"],
        barmode="group",
        title="Resource Utilization"
    ),
    width="stretch"
)
def schedule(algorithm):
    load = [0, 0, 0]
    result = []
    for i, task in tasks.iterrows():
        vm = i % 3 if algorithm == "Round Robin" else load.index(min(load))
        time = task.Workload / vms.MIPS[vm]
        load[vm] += time
        result.append([task.Task, f"VM-{vm+1}", round(time, 2)])
    return pd.DataFrame(result, columns=["Task", "VM", "Time"]), max(load)
algorithm = st.selectbox(
    "Scheduling Algorithm",
    ["Round Robin", "Least Loaded"]
)
result, makespan = schedule(algorithm)
_, rr = schedule("Round Robin")
_, ll = schedule("Least Loaded")
c1, c2, c3 = st.columns(3)
c1.metric("Virtual Machines", len(vms))
c2.metric("Average CPU", f"{vms.CPU.mean():.1f}%")
c3.metric("Current Makespan", f"{makespan:.1f}")
if vms.CPU.max() >= 80:
    st.error("SYSTEM STATUS: CRITICAL")
elif vms.CPU.mean() >= 60:
    st.warning("SYSTEM STATUS: WARNING")
else:
    st.success("SYSTEM STATUS: HEALTHY")
st.subheader("Task Performance")
st.dataframe(result, hide_index=True)
st.plotly_chart(
    px.bar(
        result,
        x="Task",
        y="Time",
        color="Time",
        title="Task Execution Time"
    ),
    width="stretch"
)
comparison = pd.DataFrame({
    "Algorithm": ["Round Robin", "Least Loaded"],
    "Makespan": [rr, ll]
})
st.subheader("Scheduling Comparison")
st.plotly_chart(
    px.bar(
        comparison,
        x="Algorithm",
        y="Makespan",
        color="Algorithm",
        text="Makespan"
    ),
    width="stretch"
)
st.metric(
    "Least-Loaded Improvement",
    f"{(rr-ll)/rr*100:.1f}%"
)

# Practical No:8:

# A) Performance Benchmarking and Load Testing of a REST API Using Locust.

# Install:
# pip install fastapi uvicorn locust

# target_api.py

import time
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI(title="Benchmark Target API")
items = {}
class Item(BaseModel):
    name: str
    price: int
@app.get("/")
def root():
    return {"message": "Benchmark Target API is running"}
@app.get("/fast")
def fast_endpoint():
    return {
        "status": "ok",
        "type": "fast",
        "data": [1, 2, 3, 4, 5]
    }
@app.get("/slow")
def slow_endpoint():
    time.sleep(0.5)
    return {
        "status": "ok",
        "type": "slow"
    }
@app.post("/items")
def create_item(item: Item):
    item_id = len(items) + 1
    items[item_id] = item.dict()
    return {
        "id": item_id,
        "item": item.dict()
    }

# locustfile.py

import random
from locust import HttpUser, task, between
class APIUser(HttpUser):
    wait_time = between(1, 2)
    def on_start(self):
        self.client.get("/")
    @task(6)
    def call_fast_endpoint(self):
        self.client.get("/fast")
    @task(3)
    def create_item(self):
        payload = {
            "name": f"item-{random.randint(1, 10000)}",
            "price": random.randint(10, 500)
        }
        self.client.post("/items", json=payload)
    @task(1)
    def call_slow_endpoint(self):
        self.client.get("/slow")
