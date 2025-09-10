import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  TextField,
  Button,
  Switch,
  FormControlLabel,
  Divider,
  Alert,
} from '@mui/material';

const Settings: React.FC = () => {
  const [settings, setSettings] = useState({
    systemName: 'Smart Locker System',
    adminEmail: 'admin@smartlocker.com',
    maxBookingDuration: 24,
    autoCleanupDays: 7,
    enableNotifications: true,
    enableWhatsApp: true,
    enableEmailAlerts: true,
    maintenanceMode: false,
  });

  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    // Save settings logic here
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        System Settings
      </Typography>

      {saved && (
        <Alert severity="success" sx={{ mb: 2 }}>
          Settings saved successfully!
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              General Settings
            </Typography>
            <TextField
              fullWidth
              label="System Name"
              value={settings.systemName}
              onChange={(e) => setSettings({ ...settings, systemName: e.target.value })}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Admin Email"
              value={settings.adminEmail}
              onChange={(e) => setSettings({ ...settings, adminEmail: e.target.value })}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Max Booking Duration (hours)"
              type="number"
              value={settings.maxBookingDuration}
              onChange={(e) => setSettings({ ...settings, maxBookingDuration: parseInt(e.target.value) })}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Auto Cleanup Days"
              type="number"
              value={settings.autoCleanupDays}
              onChange={(e) => setSettings({ ...settings, autoCleanupDays: parseInt(e.target.value) })}
              margin="normal"
            />
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Notification Settings
            </Typography>
            <FormControlLabel
              control={
                <Switch
                  checked={settings.enableNotifications}
                  onChange={(e) => setSettings({ ...settings, enableNotifications: e.target.checked })}
                />
              }
              label="Enable Notifications"
            />
            <br />
            <FormControlLabel
              control={
                <Switch
                  checked={settings.enableWhatsApp}
                  onChange={(e) => setSettings({ ...settings, enableWhatsApp: e.target.checked })}
                />
              }
              label="Enable WhatsApp Messages"
            />
            <br />
            <FormControlLabel
              control={
                <Switch
                  checked={settings.enableEmailAlerts}
                  onChange={(e) => setSettings({ ...settings, enableEmailAlerts: e.target.checked })}
                />
              }
              label="Enable Email Alerts"
            />
            <br />
            <Divider sx={{ my: 2 }} />
            <FormControlLabel
              control={
                <Switch
                  checked={settings.maintenanceMode}
                  onChange={(e) => setSettings({ ...settings, maintenanceMode: e.target.checked })}
                />
              }
              label="Maintenance Mode"
            />
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Box display="flex" justifyContent="flex-end">
            <Button variant="contained" onClick={handleSave} size="large">
              Save Settings
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Settings;