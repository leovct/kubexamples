---
description: >-
  Pods are the smallest deployable units of computing, made of containers, that
  you can create and manage in Kubernetes
---

# Pods

## Documentation

{% embed url="https://kubernetes.io/docs/concepts/workloads/pods/" %}

## Debug Pods

### Infinite Pod

Create a debug pod, based on the latest ubuntu image that never gets destroyed. It's very useful to debug and understand what's happening on a Kubernetes cluster.

```css
apiVersion: v1
kind: Pod
metadata:
  name: my-debug-pod
  spec:
    containers:
      - name: ubuntu
        image: unbutu:latest
        command: [ "sleep" ]
        args: [ "infinity" ]
```

### Inspect PVC

Useful when you want to inspect the data stored inside a persistent volume claim.

```css
apiVersion: v1
kind: Pod
metadata:
  name: my-debug-pod-with-pvc
  spec:
    containers:
      - name: ubuntu
        image: unbutu:latest
        command: [ "sleep" ]
        args: [ "infinity" ]
        volumeMounts:
          - mountPath: /data
            name: my-volume
    volumes:
      - name: my-volume
        persistentVolumeClaim:
          claimName: my-pvc
```

## Pod mounting volumes

### Mount ConfigMaps as env variables

Mounts all fields of a config map as environment variables (LOG\_LEVEL=1 and ENV=prod).

```css
apiVersion: v1
kind: Pod
metadata:
  name: my-pod-mounting-cm-as-env
spec:
  containers:
    - name: busybox
      image: k8s.gcr.io/busybox
      envFrom:
        - configMapKeyRef:
            name: my-cm
```



Only mount a specific key of a config map as environment variable (MY\_ENV\_VAR=1).

```css
apiVersion: v1
kind: Pod
metadata:
  name: my-pod-mounting-cm-as-env-v2
spec:
  containers:
    - name: busybox
      image: k8s.gcr.io/busybox
      env:
        - name: MY_ENV_VAR
          valueFrom:
            configMapKeyRef:
              name: my-cm
              key: LOG_LEVEL
```



Here's a sample config map you can use to deploy your pods.

```css
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-cm
data:
  LOG_LEVEL: '1'
  ENV: prod
```





