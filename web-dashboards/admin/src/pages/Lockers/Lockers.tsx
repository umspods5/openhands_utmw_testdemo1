import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Chip,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import {
  Lock as LockIcon,
  LockOpen as LockOpenIcon,
  Build as MaintenanceIcon,
  Schedule as ScheduleIcon,
} from '@mui/icons-material';

interface Locker {
  id: number;
  locker_number: string;
  size: string;
  status: 'available' | 'occupied' | 'maintenance' | 'reserved';
  building: string;
  floor: number;
  current_booking?: string;
  last_accessed?: string;
  temperature?: number;
  humidity?: number;
}

const Lockers: React.FC = () => {
  const [lockers, setLockers] = useState<Locker[]>([]);
  const [selectedLocker, setSelectedLocker] = useState<Locker | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [filterBuilding, setFilterBuilding] = useState<string>('all');

  useEffect(() => {
    // Mock data
    const mockLockers: Locker[] = [
      {
        id: 1,
        locker_number: 'L-001',
        size: 'small',
        status: 'occupied',
        building: 'Tower A',
        floor: 1,
        current_booking: 'BK-001',
        last_accessed: '2024-01-15 10:30',
        temperature: 22,
        humidity: 45,
      },
      {
        id: 2,
        locker_number: 'L-002',
        size: 'medium',
        status: 'available',
        building: 'Tower A',
        floor: 1,
        last_accessed: '2024-01-14 15:20',
        temperature: 23,
        humidity: 42,
      },
      {
        id: 3,
        locker_number: 'L-003',
        size: 'large',
        status: 'maintenance',
        building: 'Tower A',
        floor: 1,
        last_accessed: '2024-01-13 09:15',
      },
      // Add more mock data...
    ];
    setLockers(mockLockers);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'available': return 'success';
      case 'occupied': return 'warning';
      case 'maintenance': return 'error';
      case 'reserved': return 'info';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'available': return <LockOpenIcon />;
      case 'occupied': return <LockIcon />;
      case 'maintenance': return <MaintenanceIcon />;
      case 'reserved': return <ScheduleIcon />;
      default: return <LockIcon />;
    }
  };

  const filteredLockers = lockers.filter(locker => {
    const statusMatch = filterStatus === 'all' || locker.status === filterStatus;
    const buildingMatch = filterBuilding === 'all' || locker.building === filterBuilding;
    return statusMatch && buildingMatch;
  });

  const handleLockerClick = (locker: Locker) => {
    setSelectedLocker(locker);
    setDialogOpen(true);
  };

  const handleStatusChange = (newStatus: string) => {
    if (selectedLocker) {
      setLockers(lockers.map(locker =>
        locker.id === selectedLocker.id
          ? { ...locker, status: newStatus as any }
          : locker
      ));
      setSelectedLocker({ ...selectedLocker, status: newStatus as any });
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Locker Management
      </Typography>

      {/* Filters */}
      <Box display="flex" gap={2} mb={3}>
        <FormControl size="small" sx={{ minWidth: 120 }}>
          <InputLabel>Status</InputLabel>
          <Select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            label="Status"
          >
            <MenuItem value="all">All</MenuItem>
            <MenuItem value="available">Available</MenuItem>
            <MenuItem value="occupied">Occupied</MenuItem>
            <MenuItem value="maintenance">Maintenance</MenuItem>
            <MenuItem value="reserved">Reserved</MenuItem>
          </Select>
        </FormControl>
        <FormControl size="small" sx={{ minWidth: 120 }}>
          <InputLabel>Building</InputLabel>
          <Select
            value={filterBuilding}
            onChange={(e) => setFilterBuilding(e.target.value)}
            label="Building"
          >
            <MenuItem value="all">All</MenuItem>
            <MenuItem value="Tower A">Tower A</MenuItem>
            <MenuItem value="Tower B">Tower B</MenuItem>
            <MenuItem value="Tower C">Tower C</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* Locker Grid */}
      <Grid container spacing={2}>
        {filteredLockers.map((locker) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={locker.id}>
            <Card
              sx={{
                cursor: 'pointer',
                '&:hover': { elevation: 4 },
                border: locker.status === 'maintenance' ? '2px solid #f44336' : 'none',
              }}
              onClick={() => handleLockerClick(locker)}
            >
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                  <Typography variant="h6">{locker.locker_number}</Typography>
                  {getStatusIcon(locker.status)}
                </Box>
                <Chip
                  label={locker.status.toUpperCase()}
                  color={getStatusColor(locker.status) as any}
                  size="small"
                  sx={{ mb: 1 }}
                />
                <Typography variant="body2" color="text.secondary">
                  Size: {locker.size}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {locker.building} - Floor {locker.floor}
                </Typography>
                {locker.current_booking && (
                  <Typography variant="body2" color="primary">
                    Booking: {locker.current_booking}
                  </Typography>
                )}
                {locker.temperature && (
                  <Typography variant="body2" color="text.secondary">
                    Temp: {locker.temperature}°C | Humidity: {locker.humidity}%
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Locker Details Dialog */}
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          Locker Details - {selectedLocker?.locker_number}
        </DialogTitle>
        <DialogContent>
          {selectedLocker && (
            <Box sx={{ pt: 1 }}>
              <TextField
                fullWidth
                label="Locker Number"
                value={selectedLocker.locker_number}
                margin="normal"
                disabled
              />
              <TextField
                fullWidth
                label="Size"
                value={selectedLocker.size}
                margin="normal"
                disabled
              />
              <TextField
                fullWidth
                label="Building"
                value={selectedLocker.building}
                margin="normal"
                disabled
              />
              <TextField
                fullWidth
                label="Floor"
                value={selectedLocker.floor}
                margin="normal"
                disabled
              />
              <FormControl fullWidth margin="normal">
                <InputLabel>Status</InputLabel>
                <Select
                  value={selectedLocker.status}
                  onChange={(e) => handleStatusChange(e.target.value)}
                  label="Status"
                >
                  <MenuItem value="available">Available</MenuItem>
                  <MenuItem value="occupied">Occupied</MenuItem>
                  <MenuItem value="maintenance">Maintenance</MenuItem>
                  <MenuItem value="reserved">Reserved</MenuItem>
                </Select>
              </FormControl>
              {selectedLocker.current_booking && (
                <TextField
                  fullWidth
                  label="Current Booking"
                  value={selectedLocker.current_booking}
                  margin="normal"
                  disabled
                />
              )}
              {selectedLocker.last_accessed && (
                <TextField
                  fullWidth
                  label="Last Accessed"
                  value={selectedLocker.last_accessed}
                  margin="normal"
                  disabled
                />
              )}
              {selectedLocker.temperature && (
                <Box display="flex" gap={2}>
                  <TextField
                    label="Temperature (°C)"
                    value={selectedLocker.temperature}
                    margin="normal"
                    disabled
                    sx={{ flex: 1 }}
                  />
                  <TextField
                    label="Humidity (%)"
                    value={selectedLocker.humidity}
                    margin="normal"
                    disabled
                    sx={{ flex: 1 }}
                  />
                </Box>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Close</Button>
          <Button variant="contained" onClick={() => setDialogOpen(false)}>
            Save Changes
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Lockers;