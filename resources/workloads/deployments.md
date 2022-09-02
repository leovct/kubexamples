---
description: A Deployment provides declarative updates for Pods and ReplicaSets.
---

# Deployments

## Documentation

{% embed url="https://kubernetes.io/docs/concepts/workloads/controllers/deployment/" %}

## Simple Deployment

```css
apiVersion: apps/v1
kind: Deployment
metadata:
  name: simple-deployment
  labels:
    app: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: nginx
        image: nginx:1.23.1
        ports:
        - containerPort: 80
```
