import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Chip,
  Button,

  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import { Lock, LockOpen, Settings, Warning } from '@mui/icons-material';

interface Locker {
  id: number;
  name: string;
  size: string;
  status: 'available' | 'occupied' | 'maintenance' | 'offline';
  location: string;
  temperature?: number;
  batteryLevel?: number;
  lastUsed?: string;
}

const SimpleLockers: React.FC = () => {
  const [lockers] = useState<Locker[]>([
    {
      id: 1,
      name: 'L-001',
      size: 'small',
      status: 'available',
      location: 'Building A - Floor 1',
      temperature: 22,
      batteryLevel: 85,
      lastUsed: '2024-01-15 14:30',
    },
    {
      id: 2,
      name: 'L-002',
      size: 'medium',
      status: 'occupied',
      location: 'Building A - Floor 1',
      temperature: 18,
      batteryLevel: 92,
      lastUsed: '2024-01-16 09:15',
    },
    {
      id: 3,
      name: 'L-003',
      size: 'large',
      status: 'available',
      location: 'Building A - Floor 2',
      temperature: 25,
      batteryLevel: 78,
      lastUsed: '2024-01-14 16:45',
    },
    {
      id: 4,
      name: 'L-004',
      size: 'small',
      status: 'maintenance',
      location: 'Building B - Floor 1',
      temperature: 20,
      batteryLevel: 45,
      lastUsed: '2024-01-10 11:20',
    },
    {
      id: 5,
      name: 'L-005',
      size: 'medium',
      status: 'offline',
      location: 'Building B - Floor 2',
      batteryLevel: 12,
      lastUsed: '2024-01-08 08:30',
    },
    {
      id: 6,
      name: 'L-006',
      size: 'large',
      status: 'occupied',
      location: 'Building C - Floor 1',
      temperature: 15,
      batteryLevel: 88,
      lastUsed: '2024-01-16 13:45',
    },
  ]);

  const [filterStatus, setFilterStatus] = useState('all');
  const [filterSize, setFilterSize] = useState('all');

  const filteredLockers = lockers.filter((locker) => {
    const statusMatch = filterStatus === 'all' || locker.status === filterStatus;
    const sizeMatch = filterSize === 'all' || locker.size === filterSize;
    return statusMatch && sizeMatch;
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'available': return 'success';
      case 'occupied': return 'warning';
      case 'maintenance': return 'info';
      case 'offline': return 'error';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'available': return <LockOpen />;
      case 'occupied': return <Lock />;
      case 'maintenance': return <Settings />;
      case 'offline': return <Warning />;
      default: return <Lock />;
    }
  };

  const getSizeColor = (size: string) => {
    switch (size) {
      case 'small': return 'primary';
      case 'medium': return 'secondary';
      case 'large': return 'info';
      default: return 'default';
    }
  };

  const getBatteryColor = (level: number) => {
    if (level > 50) return 'success';
    if (level > 20) return 'warning';
    return 'error';
  };

  const handleLockerAction = (locker: Locker, action: string) => {
    console.log(`${action} locker ${locker.name}`);
    // Here you would typically make an API call
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Lockers Management
      </Typography>

      {/* Filters */}
      <Box display="flex" gap={2} sx={{ mb: 3 }}>
        <FormControl sx={{ minWidth: 120 }}>
          <InputLabel>Status</InputLabel>
          <Select
            value={filterStatus}
            label="Status"
            onChange={(e) => setFilterStatus(e.target.value)}
          >
            <MenuItem value="all">All Status</MenuItem>
            <MenuItem value="available">Available</MenuItem>
            <MenuItem value="occupied">Occupied</MenuItem>
            <MenuItem value="maintenance">Maintenance</MenuItem>
            <MenuItem value="offline">Offline</MenuItem>
          </Select>
        </FormControl>
        
        <FormControl sx={{ minWidth: 120 }}>
          <InputLabel>Size</InputLabel>
          <Select
            value={filterSize}
            label="Size"
            onChange={(e) => setFilterSize(e.target.value)}
          >
            <MenuItem value="all">All Sizes</MenuItem>
            <MenuItem value="small">Small</MenuItem>
            <MenuItem value="medium">Medium</MenuItem>
            <MenuItem value="large">Large</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* Lockers Grid */}
      <Box display="flex" flexWrap="wrap" gap={2}>
        {filteredLockers.map((locker) => (
          <Card
            key={locker.id}
            sx={{
              minWidth: 300,
              maxWidth: 350,
              cursor: 'pointer',
              '&:hover': {
                boxShadow: 4,
              },
            }}
          >
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
                <Box display="flex" alignItems="center">
                  {getStatusIcon(locker.status)}
                  <Typography variant="h6" sx={{ ml: 1 }}>
                    {locker.name}
                  </Typography>
                </Box>
                <Chip
                  label={locker.status}
                  color={getStatusColor(locker.status) as any}
                  size="small"
                />
              </Box>

              <Typography color="textSecondary" gutterBottom>
                {locker.location}
              </Typography>

              <Box display="flex" gap={1} sx={{ mb: 2 }}>
                <Chip
                  label={locker.size}
                  color={getSizeColor(locker.size) as any}
                  size="small"
                />
                {locker.batteryLevel && (
                  <Chip
                    label={`Battery: ${locker.batteryLevel}%`}
                    color={getBatteryColor(locker.batteryLevel) as any}
                    size="small"
                  />
                )}
              </Box>

              {locker.temperature && (
                <Typography variant="body2" color="textSecondary" sx={{ mb: 1 }}>
                  Temperature: {locker.temperature}°C
                </Typography>
              )}

              {locker.lastUsed && (
                <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                  Last used: {locker.lastUsed}
                </Typography>
              )}

              <Box display="flex" gap={1}>
                {locker.status === 'occupied' && (
                  <Button
                    size="small"
                    variant="outlined"
                    onClick={() => handleLockerAction(locker, 'unlock')}
                  >
                    Unlock
                  </Button>
                )}
                {locker.status === 'available' && (
                  <Button
                    size="small"
                    variant="outlined"
                    onClick={() => handleLockerAction(locker, 'test')}
                  >
                    Test
                  </Button>
                )}
                {locker.status === 'maintenance' && (
                  <Button
                    size="small"
                    variant="outlined"
                    color="success"
                    onClick={() => handleLockerAction(locker, 'activate')}
                  >
                    Activate
                  </Button>
                )}
                {locker.status === 'offline' && (
                  <Button
                    size="small"
                    variant="outlined"
                    color="error"
                    onClick={() => handleLockerAction(locker, 'diagnose')}
                  >
                    Diagnose
                  </Button>
                )}
                <Button
                  size="small"
                  variant="text"
                  onClick={() => handleLockerAction(locker, 'settings')}
                >
                  Settings
                </Button>
              </Box>
            </CardContent>
          </Card>
        ))}
      </Box>

      {filteredLockers.length === 0 && (
        <Box textAlign="center" sx={{ mt: 4 }}>
          <Typography variant="h6" color="textSecondary">
            No lockers found matching the selected filters.
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default SimpleLockers;