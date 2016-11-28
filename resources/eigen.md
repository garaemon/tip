## Craete shorter vector from longer vector

```c++
const Eigen::Vector3d = Eigen::Vector4d(0, 0, 0, 0).head<3>();
const Eigen::Vector3d = Eigen::Vector4d(0, 0, 0, 0).tail<3>();
```

## Eigen quaternion order

Eigen's quaternion order is `{w, x, y, z}`

```c++
const Eigen::Quaterniond q(1.0, 0.0, 0.0, 0.0);
```
